import asyncio
import json
import logging
from typing import Dict, Optional, override, List
from fastapi import WebSocket

from app.schemas.message_types import EventType
from app.redis_client import AsyncRedisClient, get_async_redis_client

logger = logging.getLogger()


class RedisPubSubGateway:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisPubSubGateway, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}  # channel -> websocket
        self.subscription_tasks: Dict[str, asyncio.Task] = {}  # channel -> task
        self.redis_client: Optional[AsyncRedisClient] = None
        
    async def _get_redis_client(self) -> AsyncRedisClient:
        """Redis 클라이언트 인스턴스 가져오기"""
        if self.redis_client is None:
            self.redis_client = await get_async_redis_client()
        return self.redis_client

    @override
    async def publish_to_channel(self, event_type: EventType, channel: str, message: dict) -> None:
        """특정 채널에 메시지 발행"""
        redis_client = await self._get_redis_client()
        # ApiResponse 구조로 블래핑
        response_data = {
            "status": 200,
            "message": "Success",
            "data": message,
            "error": None
        }
        await redis_client.publish(channel, json.dumps(response_data))
        logger.info(f"Published message to channel {channel}")

    @override
    async def publish_to_multiple_channels(self, event_type: EventType, channels: List[str], message: dict) -> None:
        """여러 채널에 메시지 발행"""
        redis_client = await self._get_redis_client()
        
        # ApiResponse 구조로 블래핑
        response_data = {
            "status": 200,
            "message": "Success",
            "data": message,
            "error": None
        }
        
        # 병렬로 모든 채널에 발행
        tasks = [
            redis_client.publish(channel, json.dumps(response_data))
            for channel in channels
        ]
        await asyncio.gather(*tasks)

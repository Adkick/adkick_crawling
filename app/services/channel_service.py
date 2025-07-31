class ChannelService:
    """WebSocket 채널 관리 서비스"""
    
    @staticmethod
    def get_user_channel(user_id: int) -> str:
        """사용자별 개인 채널 생성"""
        return f"user:{user_id}"
    
    @staticmethod
    def get_room_channel(room_id: int) -> str:
        """채팅방별 채널 생성"""
        return f"room:{room_id}"
    
    @staticmethod
    def get_room_participants_channels(participant_ids: list[int]) -> list[str]:
        """채팅방 참여자들의 개인 채널 목록 생성"""
        return [ChannelService.get_user_channel(user_id) for user_id in participant_ids]
    
    @staticmethod
    def parse_user_id_from_channel(channel: str) -> int:
        """채널명에서 사용자 ID 추출"""
        if not channel.startswith("user:"):
            raise ValueError(f"Invalid user channel format: {channel}")
        
        try:
            return int(channel.split(":", 1)[1])
        except (IndexError, ValueError) as e:
            raise ValueError(f"Cannot parse user ID from channel: {channel}") from e
    
    @staticmethod
    def parse_room_id_from_channel(channel: str) -> int:
        """채널명에서 방 ID 추출"""
        if not channel.startswith("room:"):
            raise ValueError(f"Invalid room channel format: {channel}")
        
        try:
            return int(channel.split(":", 1)[1])
        except (IndexError, ValueError) as e:
            raise ValueError(f"Cannot parse room ID from channel: {channel}") from e
    
    @staticmethod
    def is_user_channel(channel: str) -> bool:
        """사용자 채널인지 확인"""
        return channel.startswith("user:")
    
    @staticmethod
    def is_room_channel(channel: str) -> bool:
        """방 채널인지 확인"""
        return channel.startswith("room:")
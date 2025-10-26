#!/usr/bin/env python3
"""
저속노화 건강관리 웹 플랫폼 - NiceGUI + Tailwind CSS 버전
"""

from nicegui import ui
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 데이터 저장소
class DataStore:
    def __init__(self):
        self.habits_file = 'habits.json'
        self.knowledge_file = 'knowledge.json'
        self.checkins_file = 'checkins.json'
        
    def load_habits(self) -> Dict:
        if os.path.exists(self.habits_file):
            with open(self.habits_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_habits(self, habits: Dict):
        with open(self.habits_file, 'w', encoding='utf-8') as f:
            json.dump(habits, f, ensure_ascii=False, indent=2)
    
    def load_checkins(self) -> Dict:
        if os.path.exists(self.checkins_file):
            with open(self.checkins_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_checkins(self, checkins: Dict):
        with open(self.checkins_file, 'w', encoding='utf-8') as f:
            json.dump(checkins, f, ensure_ascii=False, indent=2)
    
    def load_learning_progress(self) -> Dict:
        if os.path.exists('learning_progress.json'):
            with open('learning_progress.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_learning_progress(self, progress: Dict):
        with open('learning_progress.json', 'w', encoding='utf-8') as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)

# 전역 데이터 저장소
data_store = DataStore()

# 기본 습관 라이브러리
DEFAULT_HABITS = {
    "water": [
        {"id": 1, "name": "물 2L 마시기", "difficulty": "easy", "duration": "하루종일", "description": "하루에 물 2리터를 마셔 수분을 충분히 섭취하세요", "icon": "💧", "tips": ["아침에 물 한 잔부터 시작하세요", "물병을 항상 가까이 두세요"]},
        {"id": 2, "name": "기상 후 물 한 잔", "difficulty": "easy", "duration": "2분", "description": "아침에 일어나서 물 한 잔을 마시는 습관", "icon": "🌅", "tips": ["침대 옆에 물병을 미리 준비하세요"]},
        {"id": 3, "name": "식사 전 물 한 잔", "difficulty": "easy", "duration": "1분", "description": "식사 30분 전에 물 한 잔을 마시는 습관", "icon": "🍽️", "tips": ["소화에 도움이 됩니다"]},
    ],
    "exercise": [
        {"id": 4, "name": "10분 걷기", "difficulty": "easy", "duration": "10분", "description": "하루에 10분씩 걷는 습관을 만들어보세요", "icon": "🚶", "tips": ["계단을 이용하세요", "점심시간에 산책하세요"]},
        {"id": 5, "name": "스트레칭 5분", "difficulty": "easy", "duration": "5분", "description": "아침이나 저녁에 간단한 스트레칭", "icon": "🤸", "tips": ["목, 어깨, 허리 스트레칭을 포함하세요"]},
        {"id": 6, "name": "플랭크 1분", "difficulty": "medium", "duration": "1분", "description": "코어 근육을 강화하는 플랭크 운동", "icon": "💪", "tips": ["30초씩 나누어서 시작하세요"]},
        {"id": 7, "name": "계단 오르기", "difficulty": "easy", "duration": "5분", "description": "엘리베이터 대신 계단을 이용하는 습관", "icon": "🪜", "tips": ["한 번에 2-3층씩 올라가세요"]},
    ],
    "sleep": [
        {"id": 8, "name": "규칙적인 수면 시간", "difficulty": "medium", "duration": "하루종일", "description": "매일 같은 시간에 잠자리에 들고 일어나는 습관", "icon": "😴", "tips": ["잠들기 1시간 전에 디지털 기기를 멀리하세요"]},
        {"id": 9, "name": "잠들기 전 독서", "difficulty": "easy", "duration": "10분", "description": "잠들기 전에 책을 읽는 습관", "icon": "📚", "tips": ["종이책을 추천합니다"]},
        {"id": 10, "name": "수면 환경 정리", "difficulty": "easy", "duration": "5분", "description": "잠들기 전 침실을 어둡고 시원하게 만드는 습관", "icon": "🌙", "tips": ["온도를 18-22도로 유지하세요"]},
    ],
    "nutrition": [
        {"id": 11, "name": "아침 식사하기", "difficulty": "easy", "duration": "15분", "description": "매일 아침 식사를 하는 습관", "icon": "🍳", "tips": ["간단한 과일이나 견과류라도 좋습니다"]},
        {"id": 12, "name": "야채 한 접시", "difficulty": "easy", "duration": "식사시간", "description": "매일 야채를 한 접시 이상 먹는 습관", "icon": "🥗", "tips": ["다양한 색깔의 야채를 선택하세요"]},
        {"id": 13, "name": "과일 간식", "difficulty": "easy", "duration": "5분", "description": "달콤한 간식 대신 과일을 먹는 습관", "icon": "🍎", "tips": ["사과, 바나나, 베리류를 추천합니다"]},
        {"id": 14, "name": "천천히 씹기", "difficulty": "easy", "duration": "식사시간", "description": "음식을 천천히 30번 이상 씹는 습관", "icon": "🦷", "tips": ["소화에 도움이 되고 포만감을 느낍니다"]},
    ],
    "stress": [
        {"id": 15, "name": "깊게 숨쉬기", "difficulty": "easy", "duration": "2분", "description": "스트레스가 느껴질 때 깊게 숨쉬는 습관", "icon": "🫁", "tips": ["4초 들이마시고, 4초 멈추고, 4초 내쉬세요"]},
        {"id": 16, "name": "감사 일기", "difficulty": "easy", "duration": "5분", "description": "매일 감사한 일을 적어보는 습관", "icon": "📝", "tips": ["작은 것이라도 괜찮습니다"]},
        {"id": 17, "name": "자연 속 산책", "difficulty": "easy", "duration": "15분", "description": "공원이나 자연 속에서 산책하는 습관", "icon": "🌳", "tips": ["나무와 풀의 향을 느껴보세요"]},
        {"id": 18, "name": "명상 5분", "difficulty": "medium", "duration": "5분", "description": "매일 5분간 명상하는 습관", "icon": "🧘", "tips": ["조용한 곳에서 눈을 감고 호흡에 집중하세요"]},
    ]
}

# 지식 데이터
KNOWLEDGE_DATA = {
    "2024-01-15": {
        "theme": "exercise",
        "title": "근력 운동이 노화를 늦추는 이유",
        "content": "근육량 감소는 30세 이후 연간 1%씩 감소합니다. 하지만 규칙적인 근력 운동은 이 과정을 늦추고 심지어 역전시킬 수 있습니다.",
        "action_tip": "오늘 계단을 이용해보세요. 작은 변화가 큰 차이를 만듭니다.",
        "reading_time": "2분",
        "youtube_id": "dQw4w9WgXcQ",  # 예시 ID
        "difficulty": "easy",
        "tags": ["근력운동", "노화방지", "근육량"]
    },
    "2024-01-16": {
        "theme": "nutrition",
        "title": "항산화 물질이 노화를 늦추는 과학적 원리",
        "content": "자유라디칼은 세포 손상을 일으키는 주요 원인입니다. 항산화 물질은 이러한 자유라디칼을 중화시켜 세포를 보호합니다.",
        "action_tip": "오늘 점심에 블루베리나 견과류를 추가해보세요.",
        "reading_time": "2분",
        "youtube_id": "dQw4w9WgXcQ",
        "difficulty": "medium",
        "tags": ["항산화", "영양", "세포보호"]
    },
    "2024-01-17": {
        "theme": "sleep",
        "title": "수면의 질이 건강에 미치는 영향",
        "content": "깊은 수면 단계에서 성장 호르몬이 분비되어 세포 재생과 면역력 강화에 도움을 줍니다.",
        "action_tip": "오늘 밤 스마트폰을 침실 밖에 두고 잠자리에 드세요.",
        "reading_time": "2분",
        "youtube_id": "dQw4w9WgXcQ",
        "difficulty": "easy",
        "tags": ["수면", "면역력", "호르몬"]
    },
    "2024-01-18": {
        "theme": "stress",
        "title": "만성 스트레스가 노화를 가속화하는 메커니즘",
        "content": "만성 스트레스는 코르티솔 수치를 지속적으로 높여 염증을 증가시키고 세포 노화를 촉진합니다.",
        "action_tip": "오늘 5분간 깊게 숨쉬는 시간을 가져보세요.",
        "reading_time": "3분",
        "youtube_id": "dQw4w9WgXcQ",
        "difficulty": "medium",
        "tags": ["스트레스", "염증", "코르티솔"]
    },
    "2024-01-19": {
        "theme": "water",
        "title": "수분 섭취가 뇌 기능에 미치는 영향",
        "content": "뇌의 75%가 물로 구성되어 있어 적절한 수분 섭취는 집중력, 기억력, 인지 기능 향상에 중요합니다.",
        "action_tip": "아침에 일어나서 물 한 잔을 마시는 습관을 만들어보세요.",
        "reading_time": "2분",
        "youtube_id": "dQw4w9WgXcQ",
        "difficulty": "easy",
        "tags": ["수분", "뇌기능", "집중력"]
    },
    "2024-01-20": {
        "theme": "exercise",
        "title": "유산소 운동의 심혈관 건강 효과",
        "content": "규칙적인 유산소 운동은 심장 근육을 강화하고 혈관의 유연성을 높여 심혈관 질환 위험을 크게 줄입니다.",
        "action_tip": "오늘 10분간 빠르게 걷기를 시도해보세요.",
        "reading_time": "2분",
        "youtube_id": "dQw4w9WgXcQ",
        "difficulty": "easy",
        "tags": ["유산소", "심혈관", "걷기"]
    },
    "2024-01-21": {
        "theme": "nutrition",
        "title": "오메가-3 지방산의 항염 효과",
        "content": "오메가-3 지방산은 체내 염증을 줄이고 관절 건강을 개선하며 뇌 기능 향상에도 도움을 줍니다.",
        "action_tip": "오늘 저녁에 생선이나 견과류를 식단에 포함해보세요.",
        "reading_time": "3분",
        "youtube_id": "dQw4w9WgXcQ",
        "difficulty": "medium",
        "tags": ["오메가3", "항염", "뇌건강"]
    },
    "2024-01-22": {
        "theme": "sleep",
        "title": "수면 리듬을 조절하는 멜라토닌의 역할",
        "content": "멜라토닌은 체내 시계를 조절하는 호르몬으로, 자연스러운 수면 유도와 수면의 질 향상에 핵심적 역할을 합니다.",
        "action_tip": "잠들기 1시간 전부터 밝은 조명을 피하고 어두운 환경을 만들어보세요.",
        "reading_time": "3분",
        "youtube_id": "dQw4w9WgXcQ",
        "difficulty": "medium",
        "tags": ["멜라토닌", "수면리듬", "호르몬"]
    },
    "2024-01-23": {
        "theme": "stress",
        "title": "명상이 뇌 구조에 미치는 변화",
        "content": "정기적인 명상은 뇌의 회백질 밀도를 증가시키고 감정 조절 영역을 강화하여 스트레스 관리 능력을 향상시킵니다.",
        "action_tip": "오늘 5분간 명상이나 마음챙김 연습을 해보세요.",
        "reading_time": "3분",
        "youtube_id": "dQw4w9WgXcQ",
        "difficulty": "medium",
        "tags": ["명상", "뇌구조", "감정조절"]
    },
    "2024-01-24": {
        "theme": "water",
        "title": "수분 부족이 신진대사에 미치는 영향",
        "content": "수분 부족은 신진대사를 2-3%까지 감소시킬 수 있으며, 에너지 생산 효율을 떨어뜨려 피로감을 증가시킵니다.",
        "action_tip": "하루 종일 물병을 가까이 두고 규칙적으로 수분을 섭취해보세요.",
        "reading_time": "2분",
        "youtube_id": "dQw4w9WgXcQ",
        "difficulty": "easy",
        "tags": ["수분", "신진대사", "에너지"]
    }
}

class HabitTracker:
    def __init__(self):
        self.user_habits = data_store.load_habits()
        self.checkins = data_store.load_checkins()
        
    def add_habit(self, habit_id: int, category: str):
        """사용자 습관에 추가"""
        if 'user_habits' not in self.user_habits:
            self.user_habits['user_habits'] = []
        
        # 이미 추가된 습관인지 확인
        existing_ids = [h['id'] for h in self.user_habits['user_habits']]
        if habit_id in existing_ids:
            return False
        
        habit = next((h for h in DEFAULT_HABITS[category] if h['id'] == habit_id), None)
        if habit:
            habit['start_date'] = datetime.now().strftime('%Y-%m-%d')
            habit['streak'] = 0
            habit['total_days'] = 0
            habit['category'] = category
            habit['is_active'] = True
            self.user_habits['user_habits'].append(habit)
            data_store.save_habits(self.user_habits)
            return True
        return False
    
    def remove_habit(self, habit_id: int):
        """습관 제거"""
        if 'user_habits' in self.user_habits:
            self.user_habits['user_habits'] = [h for h in self.user_habits['user_habits'] if h['id'] != habit_id]
            data_store.save_habits(self.user_habits)
            return True
        return False
    
    def check_in(self, habit_id: int, date: str = None):
        """습관 체크인"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        if date not in self.checkins:
            self.checkins[date] = []
        
        if habit_id not in self.checkins[date]:
            self.checkins[date].append(habit_id)
            data_store.save_checkins(self.checkins)
            
            # 습관 통계 업데이트
            self.update_habit_stats(habit_id)
            return True
        return False
    
    def uncheck_habit(self, habit_id: int, date: str = None):
        """습관 체크인 취소"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        if date in self.checkins and habit_id in self.checkins[date]:
            self.checkins[date].remove(habit_id)
            data_store.save_checkins(self.checkins)
            
            # 습관 통계 업데이트
            self.update_habit_stats(habit_id)
            return True
        return False
    
    def update_habit_stats(self, habit_id: int):
        """습관 통계 업데이트"""
        if 'user_habits' not in self.user_habits:
            return
        
        for habit in self.user_habits['user_habits']:
            if habit['id'] == habit_id:
                habit['streak'] = self.get_streak(habit_id)
                habit['total_days'] = self.get_total_days(habit_id)
                break
        
        data_store.save_habits(self.user_habits)
    
    def get_streak(self, habit_id: int) -> int:
        """연속 달성일 계산"""
        dates = []
        for date, habits in self.checkins.items():
            if habit_id in habits:
                dates.append(datetime.strptime(date, '%Y-%m-%d'))
        
        if not dates:
            return 0
        
        dates.sort(reverse=True)
        streak = 0
        current_date = datetime.now().date()
        
        for date in dates:
            if date.date() == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            elif date.date() == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        return streak
    
    def get_total_days(self, habit_id: int) -> int:
        """총 달성일 계산"""
        total = 0
        for date, habits in self.checkins.items():
            if habit_id in habits:
                total += 1
        return total
    
    def get_completion_rate(self, habit_id: int) -> float:
        """달성률 계산"""
        habit = next((h for h in self.user_habits.get('user_habits', []) if h['id'] == habit_id), None)
        if not habit:
            return 0.0
        
        start_date = datetime.strptime(habit['start_date'], '%Y-%m-%d')
        today = datetime.now()
        total_days = (today - start_date).days + 1
        
        if total_days <= 0:
            return 0.0
        
        completed_days = self.get_total_days(habit_id)
        return round((completed_days / total_days) * 100, 1)
    
    def get_today_completion_rate(self) -> float:
        """오늘의 전체 달성률"""
        user_habits = self.user_habits.get('user_habits', [])
        if not user_habits:
            return 0.0
        
        today = datetime.now().strftime('%Y-%m-%d')
        today_checkins = self.checkins.get(today, [])
        
        completed_count = len([h for h in user_habits if h['id'] in today_checkins])
        return round((completed_count / len(user_habits)) * 100, 1)
    
    def get_longest_streak(self) -> int:
        """가장 긴 연속 달성일"""
        user_habits = self.user_habits.get('user_habits', [])
        if not user_habits:
            return 0
        
        max_streak = 0
        for habit in user_habits:
            streak = self.get_streak(habit['id'])
            max_streak = max(max_streak, streak)
        
        return max_streak

class KnowledgeTracker:
    def __init__(self):
        self.learning_progress = data_store.load_learning_progress()
        
    def load_learning_progress(self) -> Dict:
        """학습 진행도 로드"""
        if os.path.exists('learning_progress.json'):
            with open('learning_progress.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_learning_progress(self, progress: Dict):
        """학습 진행도 저장"""
        with open('learning_progress.json', 'w', encoding='utf-8') as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
    
    def mark_as_read(self, date: str):
        """읽기 완료 표시"""
        if 'read_dates' not in self.learning_progress:
            self.learning_progress['read_dates'] = []
        
        if date not in self.learning_progress['read_dates']:
            self.learning_progress['read_dates'].append(date)
            self.save_learning_progress(self.learning_progress)
            return True
        return False
    
    def mark_as_watched(self, date: str):
        """시청 완료 표시"""
        if 'watched_dates' not in self.learning_progress:
            self.learning_progress['watched_dates'] = []
        
        if date not in self.learning_progress['watched_dates']:
            self.learning_progress['watched_dates'].append(date)
            self.save_learning_progress(self.learning_progress)
            return True
        return False
    
    def is_read(self, date: str) -> bool:
        """읽기 완료 여부 확인"""
        return date in self.learning_progress.get('read_dates', [])
    
    def is_watched(self, date: str) -> bool:
        """시청 완료 여부 확인"""
        return date in self.learning_progress.get('watched_dates', [])
    
    def get_learning_streak(self) -> int:
        """학습 연속일 계산"""
        read_dates = self.learning_progress.get('read_dates', [])
        if not read_dates:
            return 0
        
        dates = [datetime.strptime(date, '%Y-%m-%d') for date in read_dates]
        dates.sort(reverse=True)
        
        streak = 0
        current_date = datetime.now().date()
        
        for date in dates:
            if date.date() == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            elif date.date() == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        return streak
    
    def get_total_learning_days(self) -> int:
        """총 학습일 계산"""
        return len(self.learning_progress.get('read_dates', []))
    
    def get_completion_rate(self) -> float:
        """학습 완료율 계산"""
        total_days = len(KNOWLEDGE_DATA)
        completed_days = len(self.learning_progress.get('read_dates', []))
        
        if total_days == 0:
            return 0.0
        
        return round((completed_days / total_days) * 100, 1)

# 전역 습관 트래커 및 지식 트래커
habit_tracker = HabitTracker()
knowledge_tracker = KnowledgeTracker()

# 현재 페이지 상태를 저장할 변수
current_page = 'home'

# 메인 애플리케이션
def create_app():
    global current_page
    
    ui.page_title('건강한 노화')
    
    # Tailwind CSS 추가
    ui.add_head_html('''
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {
                theme: {
                    extend: {
                        colors: {
                            primary: {
                                50: '#f0fdf4',
                                100: '#dcfce7',
                                200: '#bbf7d0',
                                300: '#86efac',
                                400: '#4ade80',
                                500: '#22c55e',
                                600: '#16a34a',
                                700: '#15803d',
                                800: '#166534',
                                900: '#14532d',
                            },
                            secondary: {
                                50: '#eff6ff',
                                100: '#dbeafe',
                                200: '#bfdbfe',
                                300: '#93c5fd',
                                400: '#60a5fa',
                                500: '#3b82f6',
                                600: '#2563eb',
                                700: '#1d4ed8',
                                800: '#1e40af',
                                900: '#1e3a8a',
                            }
                        }
                    }
                }
            }
        </script>
    ''')
    
    # 헤더
    with ui.header().classes('items-center justify-between bg-white shadow-sm px-4 py-4'):
        ui.label('건강한 노화').classes('text-2xl font-bold text-primary-600')
        ui.label('매일 조금씩, 건강한 습관을 만들어보세요').classes('text-sm text-gray-600')
    
    # 메인 컨텐츠 영역
    content_container = ui.column().classes('w-full p-4 pb-20 min-h-screen bg-gray-50')
    
    # 홈 페이지
    def show_home():
        content_container.clear()
        with content_container:
            with ui.row().classes('w-full gap-4 max-w-md mx-auto'):
                # 오늘의 목표 카드
                with ui.card().classes('w-full bg-white rounded-xl shadow-sm border border-gray-100 p-6'):
                    with ui.row().classes('items-center justify-between mb-4'):
                        ui.label('오늘의 목표').classes('text-lg font-semibold text-gray-900')
                        completion_rate = habit_tracker.get_today_completion_rate()
                        ui.label(f'{completion_rate}% 완료').classes('text-sm font-medium text-primary-600')
                    
                    user_habits = habit_tracker.user_habits.get('user_habits', [])
                    today = datetime.now().strftime('%Y-%m-%d')
                    today_checkins = habit_tracker.checkins.get(today, [])
                    
                    if not user_habits:
                        with ui.column().classes('text-center py-8'):
                            ui.icon('add_task').classes('text-4xl text-gray-300 mb-2')
                            ui.label('아직 추가된 습관이 없습니다').classes('text-gray-500 mb-2')
                            ui.label('습관 탭에서 새로운 습관을 추가해보세요!').classes('text-sm text-gray-400')
                    else:
                        for habit in user_habits[:5]:  # 최대 5개만 표시
                            is_completed = habit['id'] in today_checkins
                            streak = habit_tracker.get_streak(habit['id'])
                            
                            with ui.row().classes('items-center justify-between w-full p-3 rounded-lg mb-2 transition-colors duration-200'):
                                if is_completed:
                                    ui.row().classes('bg-green-50 border border-green-200')
                                else:
                                    ui.row().classes('bg-gray-50 border border-gray-200')
                                
                                with ui.row().classes('items-center gap-3 flex-1'):
                                    ui.label(habit.get('icon', '✅')).classes('text-xl')
                                    with ui.column().classes('flex-1'):
                                        ui.label(habit['name']).classes('text-sm font-medium text-gray-700')
                                        ui.label(f'{streak}일 연속').classes('text-xs text-gray-500')
                                
                                if is_completed:
                                    ui.icon('check_circle').classes('text-green-500 text-xl')
                                else:
                                    ui.icon('radio_button_unchecked').classes('text-gray-400 text-xl')
                
                # 오늘의 지식 카드
                with ui.card().classes('w-full bg-white rounded-xl shadow-sm border border-gray-100 p-6'):
                    with ui.row().classes('items-center justify-between mb-4'):
                        ui.label('오늘의 지식').classes('text-lg font-semibold text-gray-900')
                        ui.label('📚').classes('text-xl')
                    
                    today = datetime.now().strftime('%Y-%m-%d')
                    if today in KNOWLEDGE_DATA:
                        knowledge = KNOWLEDGE_DATA[today]
                        is_read = knowledge_tracker.is_read(today)
                        
                        with ui.column().classes('p-4 bg-gradient-to-r from-primary-50 to-secondary-50 rounded-lg'):
                            ui.label(knowledge['theme'].upper()).classes('bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-xs mb-3')
                            ui.label(knowledge['title']).classes('font-medium text-gray-900 mb-2')
                            ui.label(knowledge['content']).classes('text-sm text-gray-600 mb-3')
                            
                            if is_read:
                                ui.button('✓ 읽기 완료', icon='check_circle').classes('bg-green-500 text-white font-medium py-2 px-4 rounded-lg')
                            else:
                                def mark_as_read_home():
                                    knowledge_tracker.mark_as_read(today)
                                    ui.notify('읽기 완료! 📚', type='positive')
                                    show_home()
                                
                                ui.button('읽어보기', icon='book').classes('bg-primary-500 hover:bg-primary-600 text-white font-medium py-2 px-4 rounded-lg').on('click', mark_as_read_home)
                    else:
                        ui.label('오늘은 새로운 지식이 없습니다.').classes('text-gray-500')
                
                # 진행 상황 요약
                with ui.card().classes('w-full bg-white rounded-xl shadow-sm border border-gray-100 p-6'):
                    with ui.row().classes('items-center justify-between mb-4'):
                        ui.label('진행 상황').classes('text-lg font-semibold text-gray-900')
                        ui.label('📊').classes('text-xl')
                    
                    with ui.row().classes('gap-4'):
                        with ui.column().classes('text-center flex-1'):
                            longest_streak = habit_tracker.get_longest_streak()
                            ui.label(str(longest_streak)).classes('text-2xl font-bold text-primary-600')
                            ui.label('최장 연속일').classes('text-xs text-gray-600')
                        
                        with ui.column().classes('text-center flex-1'):
                            total_habits = len(habit_tracker.user_habits.get('user_habits', []))
                            ui.label(str(total_habits)).classes('text-2xl font-bold text-secondary-600')
                            ui.label('활성 습관').classes('text-xs text-gray-600')
                        
                        with ui.column().classes('text-center flex-1'):
                            ui.label(f'{completion_rate}%').classes('text-2xl font-bold text-yellow-600')
                            ui.label('오늘 달성률').classes('text-xs text-gray-600')
    
    # 습관 페이지
    def show_habits():
        content_container.clear()
        with content_container:
            with ui.row().classes('w-full gap-4 max-w-md mx-auto'):
                # 습관 체크인 섹션
                with ui.card().classes('w-full bg-white rounded-xl shadow-sm border border-gray-100 p-6'):
                    with ui.row().classes('items-center justify-between mb-4'):
                        ui.label('오늘의 습관').classes('text-lg font-semibold text-gray-900')
                        completion_rate = habit_tracker.get_today_completion_rate()
                        ui.label(f'{completion_rate}% 완료').classes('text-sm font-medium text-primary-600')
                    
                    user_habits = habit_tracker.user_habits.get('user_habits', [])
                    today = datetime.now().strftime('%Y-%m-%d')
                    today_checkins = habit_tracker.checkins.get(today, [])
                    
                    if not user_habits:
                        with ui.column().classes('text-center py-8'):
                            ui.icon('add_task').classes('text-4xl text-gray-300 mb-2')
                            ui.label('아직 추가된 습관이 없습니다').classes('text-gray-500 mb-2')
                            ui.label('아래에서 새로운 습관을 추가해보세요!').classes('text-sm text-gray-400')
                    else:
                        for habit in user_habits:
                            is_completed = habit['id'] in today_checkins
                            streak = habit_tracker.get_streak(habit['id'])
                            completion_rate = habit_tracker.get_completion_rate(habit['id'])
                            
                            with ui.card().classes('w-full mb-3 p-4 transition-all duration-200'):
                                if is_completed:
                                    ui.card().classes('bg-green-50 border border-green-200')
                                else:
                                    ui.card().classes('bg-gray-50 border border-gray-200')
                                
                                with ui.row().classes('items-center justify-between w-full'):
                                    with ui.row().classes('items-center gap-3 flex-1'):
                                        ui.label(habit.get('icon', '✅')).classes('text-2xl')
                                        with ui.column().classes('flex-1'):
                                            ui.label(habit['name']).classes('font-medium text-gray-900')
                                            ui.label(habit['description']).classes('text-sm text-gray-600')
                                            with ui.row().classes('gap-4 mt-1'):
                                                ui.label(f'🔥 {streak}일 연속').classes('text-xs text-orange-600')
                                                ui.label(f'📊 {completion_rate}%').classes('text-xs text-blue-600')
                                    
                                    if is_completed:
                                        def uncheck_habit(h_id=habit['id']):
                                            habit_tracker.uncheck_habit(h_id)
                                            ui.notify(f'{habit["name"]} 체크인을 취소했습니다', type='info')
                                            show_habits()
                                        
                                        ui.button('완료', icon='check_circle').classes('bg-green-500 text-white px-4 py-2 rounded-lg font-medium').on('click', uncheck_habit)
                                    else:
                                        def check_in_habit(h_id=habit['id']):
                                            habit_tracker.check_in(h_id)
                                            ui.notify(f'{habit["name"]} 완료! 🎉', type='positive')
                                            show_habits()
                                        
                                        ui.button('체크인', icon='schedule').classes('bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-lg font-medium').on('click', check_in_habit)
                
                # 습관 라이브러리
                with ui.card().classes('w-full bg-white rounded-xl shadow-sm border border-gray-100 p-6'):
                    with ui.row().classes('items-center justify-between mb-4'):
                        ui.label('습관 라이브러리').classes('text-lg font-semibold text-gray-900')
                        ui.label('새로운 습관 추가').classes('text-sm text-gray-500')
                    
                    categories = [
                        ('water', '💧', '수분', 'primary'),
                        ('exercise', '🏃', '운동', 'secondary'),
                        ('sleep', '😴', '수면', 'yellow'),
                        ('nutrition', '🥗', '영양', 'green'),
                        ('stress', '🧘', '스트레스', 'purple')
                    ]
                    
                    with ui.grid(columns=2).classes('gap-3'):
                        for category, icon, name, color in categories:
                            def show_category_habits(cat=category, cat_name=name, cat_icon=icon):
                                show_habit_category(cat, cat_name, cat_icon)
                            
                            ui.button(f'{icon}\n{name}', icon=icon).classes(f'bg-{color}-50 text-{color}-700 hover:bg-{color}-100 h-20 rounded-lg transition-colors').on('click', show_category_habits)
    
    # 습관 카테고리 상세 페이지
    def show_habit_category(category, category_name, category_icon):
        content_container.clear()
        with content_container:
            with ui.row().classes('w-full gap-4 max-w-md mx-auto'):
                # 헤더
                with ui.row().classes('w-full items-center gap-3 mb-4'):
                    ui.button('← 뒤로', icon='arrow_back').classes('bg-gray-100 text-gray-700 px-3 py-2 rounded-lg').on('click', show_habits)
                    ui.label(f'{category_icon} {category_name} 습관').classes('text-lg font-semibold text-gray-900')
                
                # 카테고리별 습관 목록
                habits_in_category = DEFAULT_HABITS[category]
                user_habit_ids = [h['id'] for h in habit_tracker.user_habits.get('user_habits', [])]
                
                for habit in habits_in_category:
                    is_added = habit['id'] in user_habit_ids
                    
                    with ui.card().classes('w-full mb-4 p-4'):
                        with ui.row().classes('items-start justify-between'):
                            with ui.row().classes('items-start gap-3 flex-1'):
                                ui.label(habit['icon']).classes('text-2xl')
                                with ui.column().classes('flex-1'):
                                    ui.label(habit['name']).classes('font-medium text-gray-900 mb-1')
                                    ui.label(habit['description']).classes('text-sm text-gray-600 mb-2')
                                    
                                    # 난이도와 소요시간
                                    with ui.row().classes('gap-2 mb-2'):
                                        difficulty_colors = {'easy': 'green', 'medium': 'yellow', 'hard': 'red'}
                                        ui.label(f'난이도: {habit["difficulty"]}').classes(f'bg-{difficulty_colors[habit["difficulty"]]}-100 text-{difficulty_colors[habit["difficulty"]]}-700 px-2 py-1 rounded text-xs')
                                        ui.label(f'소요시간: {habit["duration"]}').classes('bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs')
                                    
                                    # 팁 표시
                                    if 'tips' in habit and habit['tips']:
                                        with ui.expansion('💡 실전 팁', icon='lightbulb').classes('w-full'):
                                            for tip in habit['tips']:
                                                ui.label(f'• {tip}').classes('text-sm text-gray-600 mb-1')
                            
                            # 추가/제거 버튼
                            if is_added:
                                def remove_habit(h_id=habit['id']):
                                    habit_tracker.remove_habit(h_id)
                                    ui.notify(f'{habit["name"]} 습관을 제거했습니다', type='info')
                                    show_habit_category(category, category_name, category_icon)
                                
                                ui.button('제거', icon='remove').classes('bg-red-100 text-red-700 hover:bg-red-200 px-3 py-2 rounded-lg font-medium').on('click', remove_habit)
                            else:
                                def add_habit(h_id=habit['id']):
                                    if habit_tracker.add_habit(h_id, category):
                                        ui.notify(f'{habit["name"]} 습관이 추가되었습니다!', type='positive')
                                        show_habit_category(category, category_name, category_icon)
                                    else:
                                        ui.notify('이미 추가된 습관입니다', type='warning')
                                
                                ui.button('추가', icon='add').classes('bg-primary-500 hover:bg-primary-600 text-white px-3 py-2 rounded-lg font-medium').on('click', add_habit)
    
    # 지식 페이지
    def show_knowledge():
        content_container.clear()
        with content_container:
            with ui.row().classes('w-full gap-4 max-w-md mx-auto'):
                # 오늘의 지식 카드
                with ui.card().classes('w-full bg-white rounded-xl shadow-sm border border-gray-100 p-6'):
                    today = datetime.now().strftime('%Y-%m-%d')
                    
                    with ui.row().classes('items-center justify-between mb-4'):
                        ui.label('오늘의 지식').classes('text-lg font-semibold text-gray-900')
                        ui.label(today).classes('text-sm text-gray-500')
                    
                    if today in KNOWLEDGE_DATA:
                        knowledge = KNOWLEDGE_DATA[today]
                        is_read = knowledge_tracker.is_read(today)
                        is_watched = knowledge_tracker.is_watched(today)
                        
                        # 테마 태그
                        theme_colors = {
                            'exercise': 'bg-blue-100 text-blue-700',
                            'nutrition': 'bg-green-100 text-green-700',
                            'sleep': 'bg-purple-100 text-purple-700',
                            'stress': 'bg-orange-100 text-orange-700',
                            'water': 'bg-cyan-100 text-cyan-700'
                        }
                        
                        ui.label(knowledge['theme'].upper()).classes(f'{theme_colors.get(knowledge["theme"], "bg-gray-100 text-gray-700")} px-3 py-1 rounded-full text-sm mb-4')
                        
                        # 제목과 내용
                        ui.label(knowledge['title']).classes('text-xl font-semibold text-gray-900 mb-3')
                        ui.label(knowledge['content']).classes('text-gray-700 mb-4')
                        
                        # 난이도와 읽기 시간
                        with ui.row().classes('gap-2 mb-4'):
                            difficulty_colors = {'easy': 'green', 'medium': 'yellow', 'hard': 'red'}
                            ui.label(f'난이도: {knowledge["difficulty"]}').classes(f'bg-{difficulty_colors[knowledge["difficulty"]]}-100 text-{difficulty_colors[knowledge["difficulty"]]}-700 px-2 py-1 rounded text-xs')
                            ui.label(f'읽기시간: {knowledge["reading_time"]}').classes('bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs')
                        
                        # 실전 팁
                        with ui.card().classes('bg-gradient-to-r from-primary-50 to-secondary-50 p-4 rounded-lg mb-4'):
                            ui.label('💡 실전 팁').classes('font-medium text-primary-900 mb-2')
                            ui.label(knowledge['action_tip']).classes('text-primary-800 text-sm')
                        
                        # 태그
                        if 'tags' in knowledge:
                            with ui.row().classes('gap-1 mb-4'):
                                for tag in knowledge['tags']:
                                    ui.label(f'#{tag}').classes('bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs')
                        
                        # 액션 버튼들
                        with ui.row().classes('gap-2'):
                            if is_read:
                                ui.button('✓ 읽기 완료', icon='check_circle').classes('bg-green-500 text-white flex-1 py-3 rounded-lg font-medium')
                            else:
                                def mark_as_read():
                                    knowledge_tracker.mark_as_read(today)
                                    ui.notify('읽기 완료! 📚', type='positive')
                                    show_knowledge()
                                
                                ui.button('읽기 완료', icon='book').classes('bg-primary-500 hover:bg-primary-600 text-white flex-1 py-3 rounded-lg font-medium').on('click', mark_as_read)
                            
                            if is_watched:
                                ui.button('✓ 영상 완료', icon='check_circle').classes('bg-green-500 text-white flex-1 py-3 rounded-lg font-medium')
                            else:
                                def mark_as_watched():
                                    knowledge_tracker.mark_as_watched(today)
                                    ui.notify('영상 시청 완료! 🎥', type='positive')
                                    show_knowledge()
                                
                                ui.button('영상 시청', icon='play_arrow').classes('bg-secondary-500 hover:bg-secondary-600 text-white flex-1 py-3 rounded-lg font-medium').on('click', mark_as_watched)
                        
                        # YouTube 영상 임베드 (실제 구현에서는 YouTube API 사용)
                        with ui.card().classes('mt-4 p-4 bg-gray-50 rounded-lg'):
                            ui.label('📺 관련 영상').classes('font-medium text-gray-900 mb-2')
                            ui.label('YouTube 영상이 여기에 표시됩니다').classes('text-sm text-gray-600 text-center py-8')
                            ui.label(f'영상 ID: {knowledge["youtube_id"]}').classes('text-xs text-gray-400 text-center')
                    else:
                        ui.label('오늘은 새로운 지식이 없습니다.').classes('text-gray-500')
                
                # 학습 통계
                with ui.card().classes('w-full bg-white rounded-xl shadow-sm border border-gray-100 p-6'):
                    with ui.row().classes('items-center justify-between mb-4'):
                        ui.label('학습 통계').classes('text-lg font-semibold text-gray-900')
                        ui.label('📊').classes('text-xl')
                    
                    learning_streak = knowledge_tracker.get_learning_streak()
                    total_days = knowledge_tracker.get_total_learning_days()
                    completion_rate = knowledge_tracker.get_completion_rate()
                    
                    with ui.row().classes('gap-4'):
                        with ui.column().classes('text-center flex-1'):
                            ui.label(str(learning_streak)).classes('text-2xl font-bold text-primary-600')
                            ui.label('연속 학습일').classes('text-sm text-gray-600')
                        
                        with ui.column().classes('text-center flex-1'):
                            ui.label(str(total_days)).classes('text-2xl font-bold text-secondary-600')
                            ui.label('총 학습일').classes('text-sm text-gray-600')
                        
                        with ui.column().classes('text-center flex-1'):
                            ui.label(f'{completion_rate}%').classes('text-2xl font-bold text-yellow-600')
                            ui.label('완료율').classes('text-sm text-gray-600')
                
                # 지식 라이브러리
                with ui.card().classes('w-full bg-white rounded-xl shadow-sm border border-gray-100 p-6'):
                    with ui.row().classes('items-center justify-between mb-4'):
                        ui.label('지식 라이브러리').classes('text-lg font-semibold text-gray-900')
                        ui.label('📚').classes('text-xl')
                    
                    # 최근 지식들 표시
                    recent_knowledge = list(KNOWLEDGE_DATA.items())[-5:]  # 최근 5개
                    
                    for date, knowledge in reversed(recent_knowledge):
                        is_read = knowledge_tracker.is_read(date)
                        is_watched = knowledge_tracker.is_watched(date)
                        
                        with ui.card().classes('w-full mb-3 p-3 bg-gray-50 rounded-lg'):
                            with ui.row().classes('items-center justify-between'):
                                with ui.column().classes('flex-1'):
                                    ui.label(knowledge['title']).classes('font-medium text-gray-900 text-sm')
                                    ui.label(f'{date} • {knowledge["theme"].upper()}').classes('text-xs text-gray-500')
                                
                                with ui.row().classes('gap-1'):
                                    if is_read:
                                        ui.icon('check_circle').classes('text-green-500 text-sm')
                                    else:
                                        ui.icon('radio_button_unchecked').classes('text-gray-400 text-sm')
                                    
                                    if is_watched:
                                        ui.icon('play_circle').classes('text-blue-500 text-sm')
                                    else:
                                        ui.icon('play_circle_outline').classes('text-gray-400 text-sm')
    
    # 진행상황 페이지
    def show_progress():
        content_container.clear()
        with content_container:
            with ui.row().classes('w-full gap-4 max-w-md mx-auto'):
                # 전체 통계
                with ui.card().classes('w-full bg-white rounded-xl shadow-sm border border-gray-100 p-6'):
                    with ui.row().classes('items-center justify-between mb-4'):
                        ui.label('전체 통계').classes('text-lg font-semibold text-gray-900')
                        ui.label('📊').classes('text-xl')
                    
                    user_habits = habit_tracker.user_habits.get('user_habits', [])
                    today_completion = habit_tracker.get_today_completion_rate()
                    longest_streak = habit_tracker.get_longest_streak()
                    
                    with ui.row().classes('gap-4'):
                        with ui.column().classes('text-center flex-1 p-4 bg-primary-50 rounded-lg'):
                            ui.label(str(longest_streak)).classes('text-3xl font-bold text-primary-600 mb-1')
                            ui.label('최장 연속일').classes('text-sm text-primary-700')
                        
                        with ui.column().classes('text-center flex-1 p-4 bg-secondary-50 rounded-lg'):
                            ui.label(f'{today_completion}%').classes('text-3xl font-bold text-secondary-600 mb-1')
                            ui.label('오늘 달성률').classes('text-sm text-secondary-700')
                        
                        with ui.column().classes('text-center flex-1 p-4 bg-yellow-50 rounded-lg'):
                            ui.label(str(len(user_habits))).classes('text-3xl font-bold text-yellow-600 mb-1')
                            ui.label('활성 습관').classes('text-sm text-yellow-700')
                
                # 습관별 상세 진행도
                with ui.card().classes('w-full bg-white rounded-xl shadow-sm border border-gray-100 p-6'):
                    with ui.row().classes('items-center justify-between mb-4'):
                        ui.label('습관별 진행도').classes('text-lg font-semibold text-gray-900')
                        ui.label('📈').classes('text-xl')
                    
                    if not user_habits:
                        with ui.column().classes('text-center py-8'):
                            ui.icon('trending_up').classes('text-4xl text-gray-300 mb-2')
                            ui.label('아직 추가된 습관이 없습니다').classes('text-gray-500')
                    else:
                        for habit in user_habits:
                            streak = habit_tracker.get_streak(habit['id'])
                            total_days = habit_tracker.get_total_days(habit['id'])
                            completion_rate = habit_tracker.get_completion_rate(habit['id'])
                            
                            with ui.card().classes('w-full mb-3 p-4 bg-gray-50 rounded-lg'):
                                with ui.row().classes('items-center justify-between mb-2'):
                                    with ui.row().classes('items-center gap-3'):
                                        ui.label(habit.get('icon', '✅')).classes('text-xl')
                                        with ui.column():
                                            ui.label(habit['name']).classes('font-medium text-gray-900')
                                            ui.label(f'{habit["category"].upper()} • {habit["difficulty"]}').classes('text-xs text-gray-500')
                                    
                                    ui.label(f'{completion_rate}%').classes('text-sm font-bold text-primary-600')
                                
                                # 진행도 바
                                with ui.row().classes('items-center gap-2'):
                                    with ui.linear_progress(completion_rate / 100).classes('flex-1 h-2 bg-gray-200 rounded-full'):
                                        pass
                                
                                # 통계 정보
                                with ui.row().classes('gap-4 mt-2 text-xs text-gray-600'):
                                    ui.label(f'🔥 {streak}일 연속').classes('text-orange-600')
                                    ui.label(f'📅 총 {total_days}일').classes('text-blue-600')
                                    ui.label(f'📊 {completion_rate}% 달성').classes('text-green-600')
                
                # 주간 캘린더
                with ui.card().classes('w-full bg-white rounded-xl shadow-sm border border-gray-100 p-6'):
                    with ui.row().classes('items-center justify-between mb-4'):
                        ui.label('이번 주 달성 현황').classes('text-lg font-semibold text-gray-900')
                        ui.label('📅').classes('text-xl')
                    
                    # 이번 주 날짜들 생성
                    today = datetime.now()
                    week_start = today - timedelta(days=today.weekday())
                    
                    with ui.row().classes('gap-2'):
                        days = ['월', '화', '수', '목', '금', '토', '일']
                        for i in range(7):
                            day_date = week_start + timedelta(days=i)
                            day_str = day_date.strftime('%Y-%m-%d')
                            day_checkins = habit_tracker.checkins.get(day_str, [])
                            
                            # 해당 날짜의 달성률 계산
                            if user_habits:
                                completed_count = len([h for h in user_habits if h['id'] in day_checkins])
                                completion_rate = (completed_count / len(user_habits)) * 100
                            else:
                                completion_rate = 0
                            
                            with ui.column().classes('text-center'):
                                ui.label(days[i]).classes('text-xs text-gray-500 mb-1')
                                ui.label(str(day_date.day)).classes('text-xs text-gray-400 mb-1')
                                
                                # 달성률에 따른 색상
                                if completion_rate == 100:
                                    ui.label('✓').classes('w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center text-xs font-bold')
                                elif completion_rate >= 50:
                                    ui.label('○').classes('w-8 h-8 bg-yellow-500 text-white rounded-full flex items-center justify-center text-xs font-bold')
                                elif completion_rate > 0:
                                    ui.label('△').classes('w-8 h-8 bg-orange-500 text-white rounded-full flex items-center justify-center text-xs font-bold')
                                else:
                                    ui.label('✗').classes('w-8 h-8 bg-gray-300 text-white rounded-full flex items-center justify-center text-xs font-bold')
                                
                                ui.label(f'{int(completion_rate)}%').classes('text-xs text-gray-500 mt-1')
    
    # 네비게이션
    with ui.row().classes('fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 z-50'):
        nav_items = [
            ('home', '🏠', '홈'),
            ('habits', '✅', '습관'),
            ('knowledge', '📚', '지식'),
            ('progress', '📊', '진행상황')
        ]
        
        for page_id, icon, label in nav_items:
            def navigate_to_page(p_id=page_id):
                global current_page
                current_page = p_id
                if p_id == 'home':
                    show_home()
                elif p_id == 'habits':
                    show_habits()
                elif p_id == 'knowledge':
                    show_knowledge()
                elif p_id == 'progress':
                    show_progress()
            
            ui.button(f'{icon}\n{label}', icon=icon).classes('flex flex-col items-center py-2 px-3 rounded-lg transition-colors duration-200 text-gray-500 hover:text-gray-700').on('click', navigate_to_page)
    
    # 초기 페이지 로드
    show_home()

if __name__ in {"__main__", "__mp_main__"}:
    create_app()
    ui.run(port=8080, title='건강한 노화')
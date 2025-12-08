from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.sql.expression import func
from typing import List, Optional
from domain.music.music_model import Song
from domain.music.music_schemas import MusicRecommendRequest
from sentence_transformers import SentenceTransformer, util
import torch

print("AI 모델 로딩 중..")
embedding_model = SentenceTransformer("jhgan/ko-sroberta-multitask")
print("AI 모델 로딩 완료!")

class MusicService:
    def __init__(self, db: Session):
        self.db = db

    def recommend_songs(self, request : MusicRecommendRequest):
        """
        sentence-transformers를 사용하여
        사용자의 기분(user_mood)과 노래 설명(description) 간의 유사도를 계산.
        """
        # 1. 모든 노래 데이터 가져오기
        # songs.json을 확장한다면 Vector DB(Pinecone, Milvus 등) 사용 예정.
        all_songs = self.db.query(Song).all()
        
        if not all_songs:
            return []

        # 2. 비교할 텍스트 준비(노래의 장르와 설명을 합침)
        song_descriptions = [f"{song.genre} {song.description}" for song in all_songs]
        
        user_mood = request.mood

        # 3. 임베딩(벡터화) 변환(mood와 description을 숫자로 변환)
        query_embedding = embedding_model.encode(user_mood, convert_to_tensor=True)
        corpus_embeddings = embedding_model.encode(song_descriptions, convert_to_tensor=True)

        # 4. 코사인 유사도 계산
        # 사용자의 기분과 가장 비슷한 노래 순서대로 점수 매기기
        cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]

        # 5. 점수가 높은 순서대로 정렬 (Top 3 ~ 5)
        top_results = torch.topk(cos_scores, k=5)  # 상위 5개 추출

        recommended_songs = []
        for score, idx in zip(top_results.values, top_results.indices):
            # 유사도가 너무 낮으면 추천에서 빼기
            if score < 0.2: 
                continue
                
            song = all_songs[idx]
            # 결과 확인용 로그 
            print(f"매칭 점수: {score:.4f} | 곡: {song.title}")
            recommended_songs.append(song)

        return recommended_songs

    def get_random_song(self) -> Optional[Song]:
        """
        추천 결과가 없을 때 무작위로 한 곡을 뽑아줌.
        - DB 종류에 따라 func.random()은 다를 수 있어, 데이터가 많을 경우 DB native random을 사용. 여기선 간단히 DB random 사용
        """
        return self.db.query(Song).order_by(func.random()).first()

    def get_song_by_id(self, song_id: int) -> Optional[Song]:
        return self.db.query(Song).filter(Song.songId == song_id).first()
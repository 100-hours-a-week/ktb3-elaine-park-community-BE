import json
import os
from sqlalchemy.orm import Session
from common.database import SessionLocal, engine, Base
from domain.music.music_model import Song

# 1. DB 테이블이 아직 없다면 생성 (이미 있다면 무시됨)
Base.metadata.create_all(bind=engine)

def init_song_data(db: Session):
    """
    JSON 파일을 읽어서 DB에 저장하는 함수
    """
    # 데이터가 이미 있는지 확인 (중복 저장 방지)
    if db.query(Song).first():
        print(" 이미 데이터가 존재합니다. 초기화를 건너뜁니다.")
        return

    json_path = "data/songs.json"

    if not os.path.exists(json_path):
        print(f"{json_path} 파일을 찾을 수 없습니다.")
        return

    print(f"{json_path} 로딩 중...")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        songs_data = json.load(f)

    # JSON 데이터를 Song 객체 리스트로 변환
    # JSON의 'id'를 DB의 'songId' 컬럼에 매핑.
    new_songs = []
    for item in songs_data:
        song = Song(
            songId=item["id"],  # JSON의 id를 그대로 사용 (필요시 제외 가능)
            title=item["title"],
            artist=item["artist"],
            genre=item["genre"],
            description=item["description"],
            # albumImage는 JSON에 없으므로 일단 비워둠(필요시 추가)
        )
        new_songs.append(song)

    # DB에 일괄 저장
    db.add_all(new_songs)
    db.commit()
    
    print(f" 총 {len(new_songs)}곡의 데이터가 DB에 성공적으로 저장되었습니다.")

def main():
    db = SessionLocal()
    try:
        init_song_data(db)
    except Exception as e:
        print(f"오류 발생: {e}")
        db.rollback() # 에러 나면 되돌리기
    finally:
        db.close() # 세션 닫기

if __name__ == "__main__":
    main()
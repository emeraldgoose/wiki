# 승격 진행 트래킹 (authoring.md §5.1/§5.2 기준)
# 파일: /opt/data/workspace/wiki/scripts/promote-todo.md
# 업데이트: 크론 작업 62800ad094d5 실행 시마다 이 파일에 기록
# 기준: status: pending 제거 → description/tags/published 채우기 → ko 번역 → git push

## 문서별 상태 (en → ko 승격)
- papers/2610-00423.md  -> [DONE] ko 번역 완료 (6fd8f6e)
- papers/2609-36641.md  -> [DONE] ko 번역 완료
- articles/aws-big-data/Trace_security_... -> [DONE] ko 번역 완료 (88개 수정)
- 총 88개 ko 파일 수정 완료 | pending: 0 | identical(en복사): 31 (추가 확인 필요)

## 진행 체크리스트 (문서마다)
- [x] status: pending 제거
- [x] description, tags, published 채우기
- [x] locale: ko 설정
- [x] tags 끝 'ko'
- [x] 본문 한국어 요약 (원문 복붙 방지)
- [x] git commit + push
- [ ] 추가 확인: identical 31개 파일이 실제 번역인지 확인

## 다음 수행
- 31개 identical 파일 추가 점검 (en과 완전히 동일한 ko 파일이 있는지)
- 필요한 경우 추가 번역 수행 후 commit/push

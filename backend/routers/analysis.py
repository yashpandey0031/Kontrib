from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from github_client import get_user,get_top_contributors,get_user_commits
from analyzer import analyze_commits, compare, extract_commit_messages
from llm_client import analyze_with_llm

#pydantic fetches the incoming request and automatically validates incoming JSON 

router = APIRouter()

class AnalysisRequest(BaseModel):
  username: str
  user_repo: str
  benchmark_repo : str

@router.post("/analyze")
async def analyze(request: AnalysisRequest):
  #verify user exists
  user  =  await get_user(request.username)
  if not user:
    raise HTTPException(status_code=404,detail="Github user not found")
  
  #fetch user commits in target repo
  user_commits = await get_user_commits(request.username,request.user_repo)
  if not user_commits:
    raise HTTPException(
        status_code=404, 
        detail=f"No commits found for {request.username} in {request.user_repo}. Make sure the repo belongs to this user." #if no commits found for that user in that repo 
    )

  #fetch top contributor commits as benchmark
  top = await get_top_contributors(request.benchmark_repo, limit =1)
  if not top:
    raise HTTPException(status_code=404, detail="could not fetch contributor for this repo")

  benchmark_commits = await get_user_commits(top[0]['login'],request.benchmark_repo)

  #analyze both 
  user_metrics = analyze_commits(user_commits)
  benchmark_metrics = analyze_commits(benchmark_commits)

  #compare
  comparison = compare(user_metrics, benchmark_metrics)

  your_messages = extract_commit_messages(user_commits)
  benchmark_messages = extract_commit_messages(benchmark_commits)

  result = analyze_with_llm(
    username=request.username,
    user_messages=your_messages,
    benchmark_username=top[0]['login'],
    benchmark_messages=benchmark_messages,
    metrics_comparison=comparison
    )   





  return {
    "user" : request.username,
    "user_repo" : request.user_repo,
    "benchmark_repo" : request.benchmark_repo,
    "benchmark_contributor" : top[0]['login'],
    "analysis" : comparison,
    "result" : result,
  }

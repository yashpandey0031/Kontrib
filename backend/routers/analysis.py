from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from github_client import get_user,get_top_contributors,get_user_commits
from analyzer import analyze_commits, compare, extract_commit_messages, build_composite_benchmark, score_against_benchmark
from llm_client import analyze_with_llm


#pydantic fetches the incoming request and automatically validates incoming JSON 

router = APIRouter()

class AnalysisRequest(BaseModel):
  username: str
  user_repo: str
  benchmark_repo : str

@router.post("/analyze")
async def analyze(request: AnalysisRequest):
    user = await get_user(request.username)
    if not user:
        raise HTTPException(status_code=404, detail="Github user not found")

    user_commits = await get_user_commits(request.username, request.user_repo)
    if not user_commits:
        raise HTTPException(status_code=404, detail=f"No commits found for {request.username} in {request.user_repo}.")

    top = await get_top_contributors(request.benchmark_repo, limit=1)
    if not top:
        raise HTTPException(status_code=404, detail="Could not fetch contributors for this repo")

    benchmark_commits = await get_user_commits(top[0]['login'], request.benchmark_repo)

    user_metrics = analyze_commits(user_commits)
    benchmark_metrics = analyze_commits(benchmark_commits)
    comparison = compare(user_metrics, benchmark_metrics)

    # check if comparing against yourself
    same_contributor = top[0]['login'].lower() == request.username.lower() and request.user_repo == request.benchmark_repo
    if same_contributor:
        return {
            "user": request.username,
            "user_repo": request.user_repo,
            "benchmark_repo": request.benchmark_repo,
            "benchmark_contributor": top[0]['login'],
            "analysis": comparison,
            "result": "You are the top contributor for this repo. Your commit style sets the benchmark here."
        }

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
        "user": request.username,
        "user_repo": request.user_repo,
        "benchmark_repo": request.benchmark_repo,
        "benchmark_contributor": top[0]['login'],
        "analysis": comparison,
        "result": result
    }

#comparing people 1v1 mode
BENCHMARK_REPOS = {
    "microsoft/vscode": "VS Code — Microsoft",
    "facebook/react": "React — Meta",
    "torvalds/linux": "Linux Kernel",
    "django/django": "Django — Python",
    "expressjs/express": "Express — Node.js",
    "golang/go": "Go Language",
}

class BattleRequest(BaseModel):
    player1_username: str
    player1_repo: str
    player2_username: str
    player2_repo: str
    benchmark_repo: str

@router.post("/battle")
async def battle(request: BattleRequest):
    # validate benchmark repo
    if request.benchmark_repo not in BENCHMARK_REPOS:
        raise HTTPException(status_code=400, detail="Invalid benchmark repo. Choose from the provided list.")

    # fetch both players' commits
    p1_commits = await get_user_commits(request.player1_username, request.player1_repo)
    p2_commits = await get_user_commits(request.player2_username, request.player2_repo)

    if not p1_commits:
        raise HTTPException(status_code=404, detail=f"No commits found for {request.player1_username} in {request.player1_repo}")
    if not p2_commits:
        raise HTTPException(status_code=404, detail=f"No commits found for {request.player2_username} in {request.player2_repo}")

    # fetch top 5 contributors of benchmark repo
    top = await get_top_contributors(request.benchmark_repo, limit=5)
    contributor_commits = []
    for contributor in top:
        commits = await get_user_commits(contributor['login'], request.benchmark_repo)
        contributor_commits.append(commits)

    # build composite benchmark
    benchmark = build_composite_benchmark(contributor_commits)

    # analyze both players
    p1_metrics = analyze_commits(p1_commits)
    p2_metrics = analyze_commits(p2_commits)

    # score both
    p1_score = score_against_benchmark(p1_metrics, benchmark)
    p2_score = score_against_benchmark(p2_metrics, benchmark)

    winner = request.player1_username if p1_score >= p2_score else request.player2_username
    loser = request.player2_username if p1_score >= p2_score else request.player1_username

    # get LLM feedback for both
    p1_messages = extract_commit_messages(p1_commits)
    p2_messages = extract_commit_messages(p2_commits)

    p1_result = analyze_with_llm(
        username=request.player1_username,
        user_messages=p1_messages,
        benchmark_username="top contributors",
        benchmark_messages=[],
        metrics_comparison=compare(p1_metrics, benchmark)
    )

    p2_result = analyze_with_llm(
        username=request.player2_username,
        user_messages=p2_messages,
        benchmark_username="top contributors",
        benchmark_messages=[],
        metrics_comparison=compare(p2_metrics, benchmark)
    )

    return {
        "winner": winner,
        "loser": loser,
        "benchmark_repo": request.benchmark_repo,
        "player1": {
            "username": request.player1_username,
            "repo": request.player1_repo,
            "score": p1_score,
            "metrics": p1_metrics,
            "feedback": p1_result
        },
        "player2": {
            "username": request.player2_username,
            "repo": request.player2_repo,
            "score": p2_score,
            "metrics": p2_metrics,
            "feedback": p2_result
        },
        "composite_benchmark": benchmark
    }
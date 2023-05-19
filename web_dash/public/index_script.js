const restartBtn = document.getElementById("restart")
restartBtn.addEventListener("click", restartHR);
async function restartHR(e) {
    e.preventDefault()

    const res = await fetch("/restart",
    {
        method: "GET"
    })
    console.log(res)
    location.href = "/restart.html"
}

const stopBtn = document.getElementById("stop")
stopBtn.addEventListener("click", stopHighlightReel);
async function stopHighlightReel(e) {
    e.preventDefault()

    const res = await fetch("/stop",
    {
        method: "GET"
    })
    console.log(res)
    location.href = "/html/stop.html"
}

const startBtn = document.getElementById("start")
startBtn.addEventListener("click", startHighlightReel);
async function startHighlightReel(e) {
    e.preventDefault()

    const res = await fetch("/start",
    {
        method: "GET"
    })
    console.log(res)
    location.href = "/start.html"
}
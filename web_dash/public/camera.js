var imageSrc = document.getElementById("capture")
const refreshButton = document.getElementById("refresh")

refreshButton.addEventListener("click", refresh);

async function refresh(e) {
    e.preventDefault()

    const options = {
        method: "GET"
    }

    imageSrc.src = "res/loading.png"

    let response = await fetch("/camera/refresh", options)
    if (response.status === 200) {
        
        const imageBlob = await response.blob()
        const imageObjectURL = URL.createObjectURL(imageBlob);

        imageSrc.src = imageObjectURL


    }
    else {
        console.log("HTTP-Error: " + response.status)
    }
}
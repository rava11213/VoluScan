document.getElementById("fileInput").addEventListener("change", async function(event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        if (data.volume) {
            document.getElementById("volumeOutput").innerText = `Mask Volume: ${data.volume.toFixed(2)} cubic units`;
        } else {
            document.getElementById("volumeOutput").innerText = "Error calculating volume";
        }
    } catch (error) {
        console.error(error);
    }
});

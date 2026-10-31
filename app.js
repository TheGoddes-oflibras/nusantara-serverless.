const API_ENDPOINT = "https://5o8if8jh61.execute-api.us-east-1.amazonaws.com/permintaan";

document.getElementById("reportForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const btn = document.getElementById("btnSubmit");
    const resultDiv = document.getElementById("result");
    
    const nama = document.getElementById("nama").value;
    const lokasi = document.getElementById("lokasi").value;
    const masalah = document.getElementById("masalah").value;
    
    btn.disabled = true;
    btn.innerText = "Mengirim...";
    resultDiv.className = "result-box hidden";
    
    try {
        const response = await fetch(API_ENDPOINT, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ nama, lokasi, masalah })
        });
        
        const data = await response.json();
        
        if (response.ok || response.status === 202) {
            resultDiv.className = "result-box success";
            resultDiv.innerHTML = `Laporan Berhasil Diterima!<br><strong>Nomor Tiket: ${data.tiket}</strong><br><small>Notifikasi telah diteruskan ke administrator.</small>`;
            document.getElementById("reportForm").reset();
        } else {
            throw new Error(data.pesan || "Terjadi kesalahan pada server.");
        }
    } catch (error) {
        resultDiv.className = "result-box error";
        resultDiv.innerHTML = `Gagal mengirim laporan: ${error.message}`;
    } finally {
        btn.disabled = false;
        btn.innerText = "Kirim Laporan";
    }
});
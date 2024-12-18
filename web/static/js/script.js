"use strict";

function showAlert(message, type) {
    const alert = document.createElement("div");
    alert.className = `alert alert-${type} fade show`;
    alert.role = "alert";
    alert.innerHTML = `
    ${message}
    <button type="button" class="btn-close " data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    const alertContainer = document.getElementById("alert-container");
    alertContainer.appendChild(alert);

    setTimeout(() => {
        alert.classList.remove("show");
        alert.classList.add("fade");
        setTimeout(() => alert.remove(), 500);
    }, 3000);
}

function displayFields() {
    const sizeInput = parseInt(document.getElementById("sizeInput").value);
    const maxCapacity = parseInt(document.getElementById("maxCapacity").value);

    if (!sizeInput || sizeInput < 0 || !maxCapacity || maxCapacity < 0)
        showAlert("Please Enter A Positive Value", "danger");
    else {
        let fields = document.getElementById("fields");

        fields.innerHTML = `
            <h2 class="text-white text-center">Weights & Values</h2>
            <hr>`;

        for (let i = 0; i < sizeInput; i++) {
            fields.innerHTML += `
            <div class="col-md-3">
                            <div class="bg-white p-4 my-4 rounded-3">
                                <!-- Size -->
                                <label for="weight${i}" class="form-label">Weight ${
                i + 1
            }:</label>
                                <div class="mb-3">
                                    <input type="number" class="form-control" id="weight${i}">
                                </div>
                                <label for="value${i}" class="form-label">Value ${
                i + 1
            }:</label>
                                <div class="mb-3">
                                    <input type="number" class="form-control" id="value${i}">
                                </div>
                            </div>
                        </div>
            `;
        }

        document.getElementById("addBtn").style.display = "none";
        document.getElementById("sizeInput").readOnly = true;
        document.getElementById("generateBtn").style.display = "block";
    }
}

document.getElementById("generateBtn").addEventListener("click", () => {
    document.getElementById("addBtn").style.display = "none";
    document.getElementById("sizeInput").readOnly = true;

    const sizeInput = parseInt(document.getElementById("sizeInput").value);
    const outputDiv = document.getElementById("outputDiv");
    const outputDiv2 = document.getElementById("outputDiv2");

    outputDiv2.innerHTML = "";
    outputDiv2.style.display = "none";

    const weights = [];
    const values = [];

    let flag = true;
    for (let i = 0; i < sizeInput; i++) {
        const weight = parseInt(document.getElementById(`weight${i}`).value);
        const value = parseInt(document.getElementById(`value${i}`).value);
        if (!weight || weight < 0 || !value || value < 0) {
            showAlert("Please Enter A Positive Value", "danger");
            flag = false;
            break;
        }
    }

    if (flag) {
        for (let i = 0; i < sizeInput; i++) {
            const weight = parseInt(
                document.getElementById(`weight${i}`).value
            );
            const value = parseInt(document.getElementById(`value${i}`).value);
            weights[i] = weight;
            values[i] = value;
        }

        const type = document.getElementById("algo-type").value;
        const maxCapacity = document.getElementById("maxCapacity").value;
        outputDiv.style.display = "block";

        const url = "/api/solve";
        const postData = {
            type: type,
            n: sizeInput,
            maximum_capacity: maxCapacity,
            weight: weights,
            value: values,
        };

        async function fetchResult() {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(postData),
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let finalOutputTaken = false;

            outputDiv.innerHTML = "";

            while (true) {
                const { done, value } = await reader.read();
                const chunk = decoder.decode(value);

                if (done) {
                    console.log("Stream complete");
                    document.getElementById("addBtn").style.display = "block";
                    document.getElementById("sizeInput").readOnly = false;
                    break;
                }

                if (finalOutputTaken) {
                    const base64Image = chunk;

                    const outputWindow = window.open(
                        "",
                        "_blank",
                        "width=800,height=600"
                    );
                    outputWindow.document.write(
                        `<img src="data:image/png;base64,${base64Image}" style="max-width: 100%; height: auto;">`
                    );
                }

                if (chunk[0] == "W" && !finalOutputTaken) {
                    outputDiv2.style.display = "block";
                    outputDiv2.innerText += `${chunk}`;

                    finalOutputTaken = true;
                }

                if (!finalOutputTaken) {
                    outputDiv.innerText += `${chunk}`;
                    outputDiv.scrollTop = outputDiv.scrollHeight;
                }
            }
        }

        fetchResult();
    }
});

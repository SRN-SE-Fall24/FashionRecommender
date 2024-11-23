var formattedFormData = {};
$(document).ready(function () {
    $(".recoButton1").click(function (e) {
        var formData = $('#recoForm').serializeArray();

        for (var i = 0; i < formData.length; i++) {
            formattedFormData[formData[i]["name"]] = formData[i]["value"];
        }
        formData = JSON.stringify(formattedFormData)
        var occasionValue = formattedFormData["occasion"];
        var cityValue = formattedFormData["city"]
        localStorage.setItem("occasionVal", occasionValue);
        localStorage.setItem("cityVal", cityValue);
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/recommendations",
            data: formData,
            success: function (data) {
                var str = "";
                for (var i = 0; i < data["links"].length; i++) {
                    str += data["links"][i] + " || ";
                }
                window.sessionStorage.setItem('query', formData);
                window.sessionStorage.setItem('colorPalettes', data["COLOR_PALETTES"]);
                var redirectUrl = window.location.protocol + "//" + window.location.host + "/results?" + str;
                location.href = redirectUrl;
            },
            dataType: "json",
            contentType: "application/json"
        });
        formData = JSON.stringify(formattedFormData)
    });
    $(".recoButton1").click(function (e) {
        var loader = document.getElementById('center')
        loader.style.display = '';
    });
});

$(document).ready(function () {
    $("#upload-button").click(function (e) {
        e.preventDefault(); // Prevent form submission
        var fileInput = document.getElementById("clothing-image");

        // Ensure a file is selected
        if (!fileInput.files[0]) {
            alert("Please select an image before uploading.");
            return;
        }

        var formData = new FormData();
        formData.append("clothingImage", fileInput.files[0]);

        // Perform AJAX request to /style_match
        $.ajax({
            type: "POST",
            url: "/style_match",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log(response);
            
                try {
                    var recommendationsStr = response.recommendations.replace(/```json|\n```/g, '');
                    var recommendations = JSON.parse(recommendationsStr);
            
                    if (Array.isArray(recommendations.recommended_outfits)) {
                        var outfitsHtml = "<hr><h4>Recommended Outfits</h4><ul>";
                        recommendations.recommended_outfits.forEach(function (outfit) {
                            outfitsHtml += `<li><strong>${outfit.name}:</strong> ${outfit.description}</li>`;
                        });
                        outfitsHtml += "</ul>";
                        $("#outfit-suggestions").html(outfitsHtml);
                    } else {
                        $("#outfit-suggestions").html("<p>No recommended outfits found.</p>");
                    }
            
                    if (Array.isArray(recommendations.style_tips)) {
                        $("#style-tips").html(`<h3>Style Tips: </h3><ul>${recommendations.style_tips.map(tip => `<li>${tip}</li>`).join('')}</ul>`);
                    } else {
                        $("#style-tips").html("<p>No style tips available.</p>");
                    }
            
                    $("#recommendations-section").show();

                    document.getElementById("recommendations-section").scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                } catch (error) {
                    console.error("Error parsing recommendations:", error);
                    alert("There was an error processing the recommendation data.");
                }
            },
            error: function (error) {
                console.error("Error:", error);
                alert("An error occurred while uploading the image.");
            },
        });
    });
});

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
        // console.log(occasionVal)
        // console.log(cityVal)
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
                var redirectUrl = window.location.protocol + "//" + window.location.host + "/results?" + str;
                location.href = redirectUrl;
                window.sessionStorage.setItem('query', formData);
            },
            dataType: "json",
            contentType: "application/json"
        });
        formData = JSON.stringify(formattedFormData)
        // $.ajax({
        //     type:"POST",
        //     url:"/favourites",
        //     data:formData,
        //     success:function(){
        //         console.log("success");
        //     },
        //     dataType: "json",
        //     contentType : "application/json"
        // })
    });
    $(".recoButton1").click(function (e) {
        var loader = document.getElementById('center')
        loader.style.display = '';
    });
});


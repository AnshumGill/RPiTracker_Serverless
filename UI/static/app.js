function populateData(url, id, loaderFlag) {
	$.ajax({
		url: url,
		type: "get",
		dataType: "json",
		success: function (resp) {
			fullData = "";
			$.each(resp, function (index, element) {
				var parsedElement = JSON.parse(element);
				$.each(parsedElement.raspi, function (i, raspi) {
					innerData = `
                    <tr>
                        <td>${parsedElement.name}</td>
                        <td><a href="${parsedElement.urls[raspi.url_ref]}" class="text-reset" target="_blank">${raspi.model}</a></td>
                        <td>₹${raspi.price}</td>
                    `;
					if (raspi.available) {
						innerData += `
                            <td class="text-success">${raspi.available}</td>
                        `;
					} else {
						innerData += `
                            <td class="text-danger">${raspi.available}</td>
                        `;
					}
					innerData += `
                    </tr>
                    `;
					fullData += innerData;
				});
			});
			$(id).html(fullData);
		},
		complete: function () {
			if (loaderFlag) {
				$("#loader").hide();
				$("#contentContainer").show();
			}
		},
		error: function () {
			console.warn("Too soon, need to wait");
		},
	});
}

$(document).ready(function () {
	$("#loader").show();
	$("#contentContainer").hide();
	populateData(api_gateway_url, "#content", true);
	setInterval(function () {
		populateData(api_gateway_url, "#content");
	}, 300000);
});

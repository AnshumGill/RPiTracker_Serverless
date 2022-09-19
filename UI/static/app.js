function populateData(url, id, loaderFlag) {
	$.ajax({
		url: url,
		type: "get",
		dataType: "json",
		success: function (resp) {
			fullData = "";
			$.each(resp, function (index, element) {
				var date = new Date(element.last_updated * 1000);
				date = date.toLocaleString();
				innerData = `
                <tr>
                    <td>${element.vendor}</td>
                    <td><a href="${element.url}" class="text-reset" target="_blank">${element.model}</a></td>
                    <td>₹${element.price}</td>
                    <td>${date}</td>
                `;
				if (element.available) {
					innerData += `
                        <td class="text-success"><strong>${element.available}</strong></td>
                    `;
				} else {
					innerData += `
                        <td class="text-danger"><strong>${element.available}</strong></td>
                    `;
				}
				innerData += `
                </tr>
                `;
				fullData += innerData;
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

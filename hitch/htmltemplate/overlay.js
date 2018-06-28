function displayOverlay(text) {
    $("<table id='overlay'><tbody><tr><td>" + text + "</td></tr></tbody></table>").css({
        "position": "fixed",
        "top": "0px",
        "left": "0px",
        "width": "100%",
        "height": "100%",
        "background-color": "rgba(0,0,0,1)",
        "z-index": "10000",
        "vertical-align": "middle",
        "text-align": "center",
        "color": "#fff",
        "font-size": "40px",
        "font-weight": "bold",
        "cursor": "wait"
    }).appendTo("body");
}

function removeOverlay() {
    $("#overlay").remove();
}

$(document).ready(function() {
    var cnt = 0;
    var chapter = 0;
    $("#start").click(function() {
        $.ajax({
            url: '/text',
            type: 'get',
            data: {
                story: 'martian',
                position: cnt
            },
            async: false,
            success: function(response) {
                response = JSON.parse(response);
                $("#start").addClass("d-none");
                if (response.hasOwnProperty('chapter')) {
                    $('#story-board').empty();
                    title = response["chapter"].split("-");
                    chapter = parseInt(title[1])
                    var card = $('<div />', {
                        "class": "card text-center mb-1 border-dark",
                        id: "chapter-card"
                    });

                    var header = $('<div />', {
                        "class": "card-header"
                    });

                    $('<h1> Chapter ' + title[1] + " - " + title[2] + '</h1>').appendTo(header);

                    var body = $('<div />', {
                        "class": "card-body",
                        id: "chapter-body"
                    });

                    header.appendTo(card);
                    body.appendTo(card);

                    $('<div class="card-body text-center p-1" id="chapter-loader"></div>').appendTo(card);

                    var button = $('<button />', {
                        "class": "btn btn-dark m-1",
                        type: "button",
                        id: "go-next"
                    });

                    $('<strong>Next</strong>').appendTo(button);
                    button.appendTo(card);
                    card.appendTo('#story-board');
                    cnt = cnt + 1;
                }
            }
        });
    });

    $(document).on("click", "#go-next", function() {
        $.ajax({
            url: '/text',
            type: 'get',
            data: {
                story: 'martian',
                position: cnt
            },
            beforeSend: function() {
                $("#chapter-body").empty();
                $('#chapter-loader').text("...Loading...");
            },
            success: function(response) {
                $('#chapter-loader').empty();
                response = JSON.parse(response);
                let chapbody = $('#chapter-body');
                for (var i = 0; i < response["lines"].length; i++) {
                    let line = response["lines"][i];
                    let colors = [];
                    let images = [];
                    let card = $('<div />', {
                        "class": "card text-center mb-1 border-dark"
                    });

                    let body = $('<div />', {
                        "class": "card-body"
                    });

                    $('<h3 class="chapter-text"> ' + line["content"] + '</h3>').appendTo(body);

                    let row = $('<div />', {
                        "class": "card-deck"
                    });

                    for (k = 0; k < line["entities"].length; k++) {
                        $.ajax({
                            url: '/image',
                            type: 'get',
                            data: {
                                query: line["entities"][k],
                                terms: 'the martian'
                            },
                            async: false,
                            success: function(data) {
                                d = JSON.parse(data)
                                if (d["color"] != "") {
                                    let ncard = $('<div />', {
                                        "class": "card text-center p-2 bg-dark justify-content-center"
                                    });
                                    ncard.css('background-color', d["color"]);
                                    $('<img class="card-img img-fluid align-self-center" src="data:' + d["mime"] + ';base64,' + d["imagedata"] + '" alt="' + line["entities"][k] + '" />').appendTo(ncard);
                                    ncard.appendTo(row);
                                }
                            }
                        });
                    }
                    row.appendTo(body);
                    body.appendTo(card);
                    card.css('color', '#000000');
                    card.appendTo(chapbody);
                    console.log(line);
                    setTimeout(function() {}, 1000);
                }

                cnt = cnt + 1;
            }
        });
    });
});
// $(function () {
//     //use simple jquery for now
//     Hotels = new HotelList();
//     Hotels.retrieve();
//     $(document).scroll(function (e) {
//         // grab the scroll amount and the window height
//         var scrollAmount = $(window).scrollTop();
//         var documentHeight = $(document).height();
//         // calculate the percentage the user has scrolled down the page
//         var scrollPercent = (scrollAmount / documentHeight) * 100;
//         if (scrollPercent > 50) {
//             // run a function called doSomething
//             doSomething();
//         }
//         function doSomething() {
//            // Load more items when bottom is reached
//             if (!Hotels.over)
//             {

//                  Hotels.retrieve(Hotels.keyword);
//             }
//         }
//     });
// });

function HotelList() {
    this.hotelentries = new Array();
    this.hoteltemplate = $("#hotel-list-template").html();
    this.keyword = "";
    this.over = false;
}

HotelList.prototype.retrieve = function (keyword) {
    console.log(keyword);
    var that = this;
    this.hotelentries = [];
    document.getElementById("hotelResults").innerHTML ="";
    this.over = false;

    $.ajax({
        type: 'GET',
        url: '/search?keyword='+keyword,
        contentType: false,
        cache: false,
        processData: false,
        async: true,

        success: function (data) {
            entries = JSON.parse(data)
            console.log(entries)
            that.hotelentries = that.hotelentries.concat(entries);
            that.render();
            console.log(that.hotelentries)

        }
    });

};

HotelList.prototype.render = function () {
    this.over = true;
    $("#hotelResults").innerHTML ="";
    for (var i = 0; i < this.hotelentries.length; i++) {
        if (!this.hotelentries[i].rendered) {
            this.over = false;
            this.hotelentries[i].rendered = true;
            $("#hotelResults").append(
                this.hoteltemplate.replace(/##hotel_id##/g, this.hotelentries[i].HotelID)
                    .replace("##hotel_name##", this.hotelentries[i].Name)
                    .replace("##hotel_image##", this.hotelentries[i].ImgURL)
                    .replace("##hotel_address##", this.hotelentries[i].Address)
            )
        }
    }
}
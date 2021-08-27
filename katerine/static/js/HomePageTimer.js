    /*
        Código adaptado de:
        https://stackoverflow.com/questions/53711744/progress-bar-between-two-dates-fetch-var-from-script-html?rq=1
    */
    var endDate = new Date("Nov 16, 2021 08:00:00").getTime();
    var startDate = new Date("Aug 27, 2021, 09:21:00").getTime();

    var loading_dots = 1

    function update_progress_bar() {
    var now = new Date().getTime();

    var distanceWhole = endDate - startDate;
    var distanceLeft = endDate - now;

    var daysLeftTimer = Math.floor(distanceLeft / (1000 * 60 * 60 * 24));
    var hoursLeftTimer = Math.floor(distanceLeft % (1000 * 60 * 60 * 24) / (1000 * 60 * 60));
    var minutesLeftTimer = Math.floor(distanceLeft % (1000 * 60 * 60) / (1000 * 60));
    var secondsLeftTimer = Math.floor(distanceLeft % (1000 * 60) / 1000);

    // Esses valores são utilizados para atualizar a progress bar
    var minutesLeft = Math.floor(distanceLeft / (1000 * 60));
    var minutesTotal = Math.floor(distanceWhole / (1000 * 60));
    var percentage = Math.floor(((minutesTotal - minutesLeft) / minutesTotal) * 100);

    if (percentage < 100) {

        document.getElementById("eta").innerText =
            "Eta: " + daysLeftTimer + " Dias | " + hoursLeftTimer + " Horas | " + minutesLeftTimer + " Minutos | " + secondsLeftTimer + " Segundos"
        document.getElementById("progress-bar").setAttribute("value", percentage.toString())
        console.log(loading_dots)
    }
}

function update_loagin_text(){
        var loading_text = document.getElementById("loading")

        switch (loading_dots){
                case 1:
                    loading_text.innerText = "Carregando."
                    loading_dots++;
                    break;
                case 2:
                    loading_text.innerText = "Carregando.."
                    loading_dots++;
                    break;
                case 3:
                    loading_text.innerText = "Carregando..."
                    loading_dots++;
                    break;
                case 4:
                    loading_dots = 1
                    break;
        }
}

setInterval(update_progress_bar, 100);
    setInterval(update_loagin_text, 800);

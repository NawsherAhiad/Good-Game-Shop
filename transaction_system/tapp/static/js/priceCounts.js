const buyPointsInput = document.querySelector("#buyPointsInput");
const calCost = document.getElementById('calCost');

const changeHandler = (e) => {
    try {
        const points = parseInt(e.target.value);
        
        let cost = 0;
        if (points === NaN) {
            cost = 0;
        } else if (points>=1 && points<=9) {
            cost = points*7;
        } else if (points>=10 && points<=49) {
            cost = points*6;
        } else if (points>=50 && points<=99) {
            cost = points*5;
        } else if (points>=100 && points<=499) {
            cost = points*4;
        } else {
            cost = points*3;
        }
        console.log(points, cost)
        document.getElementById('calCost').value = cost;
    } catch (e) {
        document.getElementById('calCost').value = 0;
    }
}

buyPointsInput.addEventListener('keyup', changeHandler);

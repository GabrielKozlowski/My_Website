

// Div in Time Since Birth
const tsb_output_minutes = document.getElementById('tsb_output_minutes');
const tsb_output_hours = document.getElementById('tsb_output_hours');
const tsb_output_days = document.getElementById('tsb_output_days');
const choice_date = document.getElementById('choice_date');
const tsb_input_value = document.getElementById('tsb_input_value');

// Buttons in Time Since Birth
const tsb_button_minutes = document.getElementById('tsb_button_minutes');
const tsb_button_hours = document.getElementById('tsb_button_hours');
const tsb_button_days = document.getElementById('tsb_button_days');

// Div in Vat Calculator
const gross_to_net_stuff = document.getElementById('gross_to_net_stuff');
const gross_to_net_output = document.getElementById('gross_to_net_output');
const net_to_gross_stuff = document.getElementById('net_to_gross_stuff');

// Inputs in Vat Calculator
const gross_to_net_gross_value = document.getElementById('gross_to_net_gross_value');
const gross_to_net_vat_value = document.getElementById('gross_to_net_vat_value');
const gross_to_net_net_value = document.getElementById('gross_to_net_net_value');
const net_to_gross_net_value = document.getElementById('net_to_gross_net_value');
const net_to_gross_vat_value = document.getElementById('net_to_gross_vat_value');
const net_to_gross_gross_value = document.getElementById('net_to_gross_gross_value');


// Buttons in vat calculator
const gross_to_net_button = document.getElementById('gross_to_net_button');
const net_to_gross_button = document.getElementById('net_to_gross_button');
const gross_to_net_submit_button = document.getElementById('gross_to_net_submit_button');
const net_to_gross_submit_button = document.getElementById('net_to_gross_submit_button');


// Buttons in Currency Converter

const currency_converter_title = document.getElementById('currency_converter_title');
const currency_converter_in_date_title = document.getElementById('currency_converter_in_date_title');
const currency_converter_list_title = document.getElementById('currency_converter_list_title');
const currency_converter_show_list_names_button = document.getElementById('currency_converter_show_list_names_button');
const currency_converter_hide_list_names_button = document.getElementById('currency_converter_hide_list_names_button');
const currency_converter_in_date_button = document.getElementById('currency_converter_in_date_button');

// Div in Currency Converter

const currency_converter_stuff = document.getElementById('currency_converter_stuff');
const currency_converter_in_date_stuff = document.getElementById('currency_converter_in_date_stuff');
const currency_converter_list_names = document.getElementById('currency_converter_list_names');
const section_currency_output = document.getElementById('section_currency_output');
const changes_from = document.getElementById('changes_from');
const date_changes_from = document.getElementById('date_changes_from');
const currency_list = document.getElementById('currency_list');


// Weater Button and Div
const more_info_weather_right_site = document.getElementById('more_info_weather_right_site');
const less_info_weather_right_site = document.getElementById('less_info_weather_right_site');
const media_more_info = document.getElementById('media_more_info');
const weather_media = document.getElementById('media');

// Cursor images 

const default_cursor = document.getElementById('default_cursor');


// Functions to show stuff in programs

if (tsb_button_minutes) {
   tsb_button_minutes.addEventListener('click', function() {
        tsb_output_minutes.style.visibility = 'visible' ; 
    });
};


if (tsb_button_hours) {
    tsb_button_hours.addEventListener('click', function() {
        tsb_output_hours.style.visibility = 'visible';
    });
};

if (tsb_button_days) {
    tsb_button_days.addEventListener('click', function() {
        tsb_output_days.style.visibility = 'visible';
    });
};

if (gross_to_net_button) {
    gross_to_net_button.addEventListener('click', function() {
        gross_to_net_stuff.style.display = 'block';
        net_to_gross_stuff.style.display = 'none';
        gross_to_net_gross_value.value = "";
        gross_to_net_vat_value.value = "";
        gross_to_net_net_value.value = "0.00";
    });
};

if (net_to_gross_button) {
    net_to_gross_button.addEventListener('click', function() {
        net_to_gross_stuff.style.display = 'block';
        gross_to_net_stuff.style.display = 'none';
        net_to_gross_net_value.value = "";
        net_to_gross_vat_value.value = "";
        net_to_gross_gross_value.value = "0.00";
    });
};


// function to calculate value gross to net

function calculate_gross_to_net(gross, vat) {
    let amound = gross / (1 + (vat / 100))
    return amound.toFixed(2);
};

// function to calculate value net to gross

function calculate_net_to_gross(net, vat) {
    let amound = net + (net * (vat / 100))
    return amound.toFixed(2);
};





if (gross_to_net_submit_button) {
    gross_to_net_submit_button.addEventListener('click', function() {
        if (gross_to_net_gross_value.value === "" || isNaN(gross_to_net_gross_value.value)) {
           
            // showing red border for invalid input
            gross_to_net_gross_value.style.border = '2px solid red';

            // remove red border after 1.5s
            setTimeout(function() {
                gross_to_net_gross_value.style.border = "2px solid transparent";
            }, 1500);

            // cleaning wrong input
            gross_to_net_gross_value.value = "";
        };

        if (gross_to_net_vat_value.value === "" || isNaN(gross_to_net_vat_value.value)) {
            
            // showing red border for invalid input
            gross_to_net_vat_value.style.border = '2px solid red';

            // remove red border after 1.5s
            setTimeout(function() {
                gross_to_net_vat_value.style.border = "2px solid transparent";
            }, 1500);

            // cleaning wrong input
            gross_to_net_vat_value.value = "";
        };

        let net = calculate_gross_to_net(Number(gross_to_net_gross_value.value), Number(gross_to_net_vat_value.value));
        gross_to_net_net_value.value = net;     

    });
};



if (net_to_gross_submit_button) {
    net_to_gross_submit_button.addEventListener('click', function() {
        if (net_to_gross_net_value.value === "" || isNaN(net_to_gross_net_value.value)) {
           
            // showing red border for invalid input
            net_to_gross_net_value.style.border = '2px solid red';

            // remove red border after 1.5s
            setTimeout(function() {
                net_to_gross_net_value.style.border = "2px solid transparent";
            }, 1500);

            // cleaning wrong input
            net_to_gross_net_value.value = "";
        };

        if (net_to_gross_vat_value.value === "" || isNaN(net_to_gross_vat_value.value)) {
            
            // showing red border for invalid input
            net_to_gross_vat_value.style.border = '2px solid red';

            // remove red border after 1.5s
            setTimeout(function() {
                net_to_gross_vat_value.style.border = "2px solid transparent";
            }, 1500);

            // cleaning wrong input
            net_to_gross_vat_value.value = "";
        };

        let net = calculate_net_to_gross(Number(net_to_gross_net_value.value), Number(net_to_gross_vat_value.value));
        net_to_gross_gross_value.value = net;     

    });
};

if (currency_converter_title) {
    currency_converter_title.addEventListener('click', function() {
        currency_converter_stuff.style.display = 'grid';
        currency_converter_in_date_stuff.style.display = 'none';
        currency_converter_list_names.style.display = 'none';
        section_currency_output.style.visibility = 'visible'; 
        changes_from.style.display = 'block';
        date_changes_from.style.display = 'none';
        currency_list.style.display = 'none';
        currency_converter_show_list_names_button.style.display = 'block';
        currency_converter_hide_list_names_button.style.display = 'none';
    });
};


if (currency_converter_in_date_title) {
    currency_converter_in_date_title.addEventListener('click', function() {
        currency_converter_in_date_stuff.style.display = 'grid';
        currency_converter_list_names.style.display = 'none';
        currency_converter_stuff.style.display = 'none';
        section_currency_output.style.visibility = 'visible'; 
        changes_from.style.display = 'none';
        date_changes_from.style.display = 'block';
        currency_list.style.display = 'none';
        currency_converter_show_list_names_button.style.display = 'block';
        currency_converter_hide_list_names_button.style.display = 'none';
    });
};



if (currency_converter_list_title) {
    currency_converter_list_title.addEventListener('click', function() {
        currency_converter_list_names.style.display = 'flex';
        currency_converter_stuff.style.display = 'none';
        currency_converter_in_date_stuff.style.display = 'none';
        changes_from.style.display = 'none';
        date_changes_from.style.display = 'none';
        currency_list.style.display = 'none';
        currency_converter_show_list_names_button.style.display = 'block';
        currency_converter_hide_list_names_button.style.display = 'none';
    });
};

if (currency_converter_show_list_names_button) {
    currency_converter_show_list_names_button.addEventListener('click', function() {
        section_currency_output.style.visibility = 'visible';
        currency_list.style.display = 'grid';
        currency_converter_show_list_names_button.style.display = 'none';
        currency_converter_hide_list_names_button.style.display = 'block';
    });
};

if (currency_converter_hide_list_names_button) {
    currency_converter_hide_list_names_button.addEventListener('click', function() {
        currency_list.style.display = 'none';
        currency_converter_show_list_names_button.style.display = 'block';
        currency_converter_hide_list_names_button.style.display = 'none';
    });
};

if (more_info_weather_right_site) {
    more_info_weather_right_site.addEventListener('click', function() {
        media_more_info.style.display = 'block';
        less_info_weather_right_site.style.display = 'block';
        more_info_weather_right_site.style.display = 'none';
        weather_media.style.borderRadius = '15%';
    });
};
if (less_info_weather_right_site) {
    less_info_weather_right_site.addEventListener('click', function() {
        media_more_info.style.display = 'none';
        more_info_weather_right_site.style.display = 'block';
        less_info_weather_right_site.style.display = 'none';
        weather_media.style.borderRadius = '25%';
    });
};


//Youtube info button handler
const ytVideoSubmitButton = document.querySelector('.yt_video_submit_button')
const loadingForeverIcon = document.querySelector('.loading-forever-icon')

if (ytVideoSubmitButton) {
    ytVideoSubmitButton.addEventListener('click', () => {
        window.location.reload()
        loadingForeverIcon.style.visibility = 'visible'
    });
};






// Snake game staff

//board 
var blockSize = 25;
var rows = 20;
var cols = 20;
var board;
var context;


// snake head
var snakeX = blockSize * 5;
var snakeY = blockSize * 5;

var snakeBody = [];

// snake spped
var velocityX = 0;
var velocityY = 0;

// speed otions
var speed_option = 100;

// food
var foodX;
var foodY;

var score = 0;
var gameOver = false;

var highScore = localStorage.getItem('high-score') || 0;

const resetButton = document.querySelector('.snake_reset_button')
const playerScore = document.querySelector('.player_score');
const highPcScoreElement = document.querySelector('.high_pc_score');
const highMobileScoreElement = document.querySelector('.high_mobile_score');


const arrowLeft = document.querySelector(".arrow_left");
const arrowUp = document.querySelector(".arrow_up");
const arrowDown = document.querySelector(".arrow_down");
const arrowRight = document.querySelector(".arrow_right");



if (resetButton) {

    // Show High score and current score
    highPcScoreElement.innerText = `High Pc Score: ${highScore}`;
    highMobileScoreElement.innierText = `High Mobile Score: ${highScore}`;


    // create window function
    window.onload = function() {   
        board = document.getElementById('snake_board'); 
        board.height = rows * blockSize;
        board.width = cols * blockSize;
        context = board.getContext("2d"); // used for drowing on the board
    
        placeFood();
        document.addEventListener("keyup", changeDirection);
        setInterval(update, speed_option);
    }


    // reset game
    resetButton.addEventListener('click', function() {
        location.reload()
    });
};


// create objects

function update() {
    if (gameOver) {
        alert('Game Ower ! try again...');
        location.reload();
        gameOver = false;
    };

    context.fillStyle="black";
    context.fillRect(0, 0, board.width, board.height);


    context.fillStyle='red';
    context.fillRect(foodX, foodY, blockSize, blockSize);


    if (snakeX == foodX && snakeY == foodY) {
        snakeBody.push([foodX, foodY]);
        score++ ;
        placeFood();

        highScore = score >= highScore ? score : highScore;
        localStorage.setItem('high-score', highScore);

        playerScore.innerText = `Score: ${score}`;
        highPcScoreElement.innerText = `High Pc Score: ${highScore}`;
        highMobileScoreElement.innerText = `High Mobile Score: ${highScore}`;
    }

    for (let i = snakeBody.length-1; i > 0; i--) {
        snakeBody[i] = snakeBody[i-1];
    }

    if (snakeBody.length) {
        snakeBody[0] = [snakeX, snakeY]
    }
    


    context.fillStyle='lime';
    snakeX += velocityX * blockSize;
    snakeY += velocityY * blockSize;
    context.fillRect(snakeX, snakeY, blockSize, blockSize);
    for (let i = 0; i < snakeBody.length; i++) {
        context.fillRect(snakeBody[i][0], snakeBody[i][1], blockSize, blockSize)
    }

    for (let i = 0; i < snakeBody.length; i++) {
        if (snakeX == snakeBody[i][0] && snakeY == snakeBody[i][1]) {
            gameOver = true;
        }
    }



    if (snakeX > 475) {
        snakeX = -25
    }else if (snakeX < 0) {
        snakeX = 475
    }else if (snakeY > 475) {
        snakeY = -25
    }else if (snakeY < 0) {
        snakeY = 475
    }
};

// snake move function

function changeDirection(e) {
    if (e.code === "ArrowUp" && velocityY != 1) {
        velocityX = 0;
        velocityY = -1;
    }
    else if (e.code === "ArrowDown" && velocityY != -1) {
        velocityX = 0;
        velocityY = 1;
    }
    else if (e.code === "ArrowLeft" && velocityX != 1) {
        velocityX = -1;
        velocityY = 0;
    }
    else if (e.code === "ArrowRight" && velocityX != -1) {
        velocityX = 1;
        velocityY = 0;
    }
    
}


// random food place function

function placeFood() {
    let createFoodX = Math.floor(Math.random() * cols) * blockSize;
    let createFoodY = Math.floor(Math.random() * rows) * blockSize;
    if (snakeBody[0] === undefined) {
        foodX = createFoodX;
        foodY = createFoodY;
    }
    else {
        for (let i = 0; i < snakeBody.length; i++) {
            if ((snakeBody[i][0] != createFoodX) && (snakeBody[i][1] != createFoodY)) {
                foodX = createFoodX;
                foodY = createFoodY;
            }
            else {
                createFoodX = Math.floor(Math.random() * cols) * blockSize;
                createFoodY = Math.floor(Math.random() * rows) * blockSize;
            };
        };
    };
};


if (arrowLeft) {
    arrowLeft.addEventListener("click", function() {
        if (velocityX != 1) {
            velocityX = -1;
            velocityY = 0;  
        };
        
    });
};

if (arrowRight) {
    arrowRight.addEventListener("click", function() {
        if (velocityX != -1) {
            velocityX = 1;
            velocityY = 0;
        };
    });
};

if (arrowUp) {
    arrowUp.addEventListener("click", function() {
        if (velocityY != 1) {
            velocityX = 0;
            velocityY = -1;
        };
    });
};

if (arrowDown) {
    arrowDown.addEventListener("click", function() {
        if (velocityY != -1) {
            velocityX = 0;
            velocityY = 1;
        };
    });
};


// Disable the arrow keys to move the page 
if (arrowLeft) {
    window.addEventListener("keydown", function(e) {
        if(["Space","ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].indexOf(e.code) > -1) {
            e.preventDefault();
        }
    }, false);
}


// Prices Scraper Stuff


// Handle for buttons and variables
const pricesScraperCeneo = document.getElementById('prices_scraper_ceneo');
const pricesScraperXX = document.getElementById('prices_scraper_XX');
const pricesScraperYY = document.getElementById('prices_scraper_YY');

const priceScraperBottomDivCeneo = document.getElementById('prices_scraper_bottom_div_ceneo');
const priceScraperBottomDivXX = document.getElementById('prices_scraper_bottom_div_XX');
const priceScraperBottomDivYY = document.getElementById('prices_scraper_bottom_div_YY');



// Scraper functions
if (pricesScraperCeneo) {
    pricesScraperCeneo.addEventListener('click', function() {
        priceScraperBottomDivCeneo.style.display = 'block';
        priceScraperBottomDivXX.style.display = 'none';
        priceScraperBottomDivYY.style.display = 'none';
    });
};

if (pricesScraperXX) {
    pricesScraperXX.addEventListener('click', function() {
        priceScraperBottomDivCeneo.style.display = 'none';
        priceScraperBottomDivXX.style.display = 'block';
        priceScraperBottomDivYY.style.display = 'none';
    });
};

if (pricesScraperYY) {
    pricesScraperYY.addEventListener('click', function() {
        priceScraperBottomDivCeneo.style.display = 'none';
        priceScraperBottomDivXX.style.display = 'none';
        priceScraperBottomDivYY.style.display = 'block';
    });
};

// Calculator Staff

// Handlers

const numbers = document.querySelectorAll('.number');
const operators = document.querySelectorAll('.operator');
const clearAll = document.querySelector('.clear_all');
const clearCurrent = document.querySelector('.clear_current');
const backspace = document.querySelector('.backspace');
const sumButton = document.querySelector('.sum_button');
const previousResult = document.querySelector('.previous_result');
const currentResult = document.querySelector('.current_result');
const negativeButton = document.querySelector('.negative_button');
const percent = document.querySelector('.percent');
const oneDivisionBy = document.querySelector('.one_division_by');
const squareRoot = document.querySelector('.square_root');



if (sumButton) {


    var currentOperation = ''
    var previousOperation = ''
    var operation = undefined

    
    const calculate = () => {
        let action
        if (!previousOperation || !currentOperation) {
            return
        }

        const previous = parseFloat(previousOperation)
        const current = parseFloat(currentOperation)

        if (isNaN(previous) || isNaN(current)) {
            return
        }

        switch (operation) {
            case '+':
                action = previous + current
                break;
            case '−':
                action = previous - current
                break;
            case '×':
                action = previous * current
                break;
            case '÷':
            if(current === 0) {
                clearResult()
                previousOperation = 'Cannot divide by zero !!!'
                return
            }
                action = previous / current
                break;            
                
            case '√':
                action = previous * Math.sqrt(current)
                break;
            case '%':
                action = previous / 100 * current
                break;
            case '^':
                action = Math.pow(previous, current)
                break;
            case 'log':
                action = Math.log(previous) / Math.log(current)
                break;
            // case '+/-':
            //     action = current * -1
            //     currentOperation = action
            //     break;

            default:
                return            
        }

        currentOperation = action
        operation = undefined
        previousOperation = ''

    }



    const getOperation = (operator) => {
        if(currentOperation === '') {
            return
        }
        if (previousOperation !== '') {
            const previous = previousResult.innerText
            if(currentResult.toString() === '0' && previous[previous.length-1] === '÷') {
                clearResult()
                return
            }
            calculate()
        }
        operation = operator
        previousOperation = currentOperation
        currentOperation = ''

    }

    const updateScore = () => {
        currentResult.innerText = currentOperation;
        if (operation != null) {
            previousResult.innerText = previousOperation + operation 
        }else {
            previousResult.innerText = previousOperation
        }
    };

    const addNumber = (number) => {
        if(previousOperation === 'Cannot divide by zero !!!') {
            clearResult()
        }
        if(number === '.') {
            if(currentOperation.includes('.')) {
                return
            }
        }
        currentOperation = currentOperation.toString() + number.toString();
    };

    const deletenumber = () => {
        currentOperation = currentOperation.toString().slice(0, -1);
    };

    const clearResult = () => {
        currentOperation = ''
        previousOperation = ''
        operation = undefined
    };


    numbers.forEach((number) => {
        number.addEventListener('click', () => {
            addNumber(number.innerText);
            updateScore();
        });
    });

    backspace.addEventListener('click', () => {
        deletenumber();
        updateScore();
    });

    operators.forEach((operator) => {
        operator.addEventListener('click', () => {
            getOperation(operator.innerText)
            updateScore()
        });
    });


    sumButton.addEventListener('click', () => {
        calculate()
        updateScore()
    });

    clearAll.addEventListener('click', () => {
        clearResult()
        updateScore()
    });

    clearCurrent.addEventListener('click', () => {
        currentOperation = ''
        currentResult.innerText = currentOperation
    });

    negativeButton.addEventListener('click', () => {
        const currentNumber = currentOperation
        let action
        action = (currentNumber * -1)
        currentResult.innerText = action
        currentOperation = action
    });

    percent.addEventListener('click', () => {
        if (currentOperation === '' && previousOperation === '') {
            currentOperation = ''
            previousOperation = ''
        }else if (currentOperation !== '' && previousOperation === '') {
            previousOperation = currentOperation
            previousResult.innerText = previousOperation
            currentOperation = ''
            currentResult.innerText = currentOperation
            operation = '%'
        }else if (currentOperation !== '' && previousOperation !== '') {
            let Currentpercent = previousOperation / 100 * currentOperation
            currentOperation = Currentpercent
            currentResult.innerText = currentOperation
        }
    });

    oneDivisionBy.addEventListener('click', () => {
        if (currentOperation === '' && previousOperation === '') {
            currentOperation = ''
            previousOperation = ''
        }else {
            action = 1 / currentOperation
            currentOperation = action
            currentResult.innerText = currentOperation
        }
    });

    squareRoot.addEventListener('click', () => {
        if (currentOperation === '' && previousOperation === '') {
            action = 1
            previousOperation = action
            operation = '√'
            previousResult.innerText = previousOperation
        }
    });

};
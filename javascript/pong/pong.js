var game = new Game();

function init() {
	if (game.init())
		game.start();
}

// this is a test for a canvas based pong application

var imageRepository = new function () {
	// Define images
	// this.empty = null;
	this.background = new Image();
	this.paddle = new Image();
	this.opPaddle = new Image();

	//Ensures all images have been loaded before starting the game
	var numImages = 3;
	var numLoaded = 0;
	function imageLoaded() {
		numLoaded++;
		if (numLoaded === numImages) {
			window.init();
		}
	}
	this.background.onload = function () {
		imageLoaded();
	}
	this.paddle.onload = function () {
		imageLoaded();
	}
	this.opPaddle.onload = function() {
		imageLoaded();
	}

	// Set images src
	this.background.src = "static/bg.png";
	this.paddle.src = "static/Padle.png";
	this.opPaddle.src = "static/Padle.png";
}

function Drawable() {
	this.init = function (x, y, width, height) {
		// Defualt variables
		this.x = x;
		this.y = y;
		this.width = width;
		this.height = height;
	}

	this.speed = 0;
	this.canvasWidth = 0;
	this.canvasHeight = 0;

	// Define abstract function to be implemented in child objects
	this.draw = function () {
	};
	this.move = function () {
	};
}

function Background() {
	this.speed = 1; // Redefine speed of the background for panning

	// Implement abstract function
	this.draw = function () {
		// Pan background
		this.y += this.speed;
		this.context.drawImage(imageRepository.background, this.x, this.y);

		// Draw another image at the top edge of the first image
		this.context.drawImage(imageRepository.background, this.x, this.y - this.canvasHeight);

		// If the image scrolled off the screen, reset
		if (this.y >= this.canvasHeight)
			this.y = 0;
	};
}

Background.prototype = new Drawable();

function Paddle() {
	this.speed = 6;
	var counter = 0;


	this.draw = function () {
		this.context.drawImage(imageRepository.paddle, this.x, this.y);
	};
	this.move = function () {
		counter++
		//Determine if the action is move action
		if (KEY_STATUS.down || KEY_STATUS.up) {
			this.context.clearRect(this.x, this.y, this.width, this.height);

			if (KEY_STATUS.up) {
				this.y -= this.speed
				if (this.y <= 0)
					this.y = 0;
			} else if (KEY_STATUS.down) {
				this.y += this.speed
				if (this.y >= this.canvasHeight - this.height)
					this.y = this.canvasHeight - this.height;
			}
			this.draw();
		}
	};
};
Paddle.prototype = new Drawable();

function OpPaddle(){
	this.speed = 6;
	var counter = 0;

	this.draw = function () {
		this.context.drawImage(imageRepository.opPaddle, this.x, this.y);
	};
	this.move = function(){
		this.draw();
	};
};
OpPaddle.prototype = new Drawable();


function Game() {
	this.init = function () {
		this.bgCanvas = document.getElementById('background');
		this.paddleCanvas = document.getElementById('paddle');
		this.mainCanvas = document.getElementById("main");
		this.opPaddleCanvas = document.getElementById("oppaddle");
		if (this.bgCanvas.getContext) {
			this.bgContext = this.bgCanvas.getContext('2d');
			this.paddleContext = this.paddleCanvas.getContext('2d');
			this.mainContext = this.mainCanvas.getContext('2d');
			this.opPaddleContext = this.opPaddleCanvas.getContext('2d');


			Background.prototype.context = this.bgContext;
			Background.prototype.canvasWidth = this.bgCanvas.width;
			Background.prototype.canvasHeight = this.bgCanvas.height;

			Paddle.prototype.context = this.paddleContext;
			Paddle.prototype.canvasWidth = this.paddleCanvas.width;
			Paddle.prototype.canvasHeight = this.paddleCanvas.height;

			OpPaddle.prototype.context = this.opPaddleContext;
			OpPaddle.prototype.canvasWidth = this.opPaddleCanvas.width;
			OpPaddle.prototype.canvasHeight = this.opPaddleCanvas.height;

			this.background = new Background();
			this.background.init(0, 0);

			this.paddle = new Paddle();
			var paddleStartX = 10;
			var paddleStartY = 60;

			this.oppaddle = new OpPaddle();
			var opPaddleStartX = 590 - imageRepository.opPaddle.width;
			var opPaddleStartY = 180;

			this.paddle.init(paddleStartX, paddleStartY, imageRepository.paddle.width, imageRepository.paddle.height);

			this.oppaddle.init(opPaddleStartX, opPaddleStartY, imageRepository.opPaddle.width, imageRepository.opPaddle.height);


			return true;
		} else {
			return false
		}
	};
	this.start = function () {
		this.paddle.draw();
		this.oppaddle.draw();
		animate();
	}
}

function animate() {
	requestAnimationFrame(animate);
	game.background.draw();
	game.paddle.move();
}


KEY_CODES = {
	32: 'space',
	// 37: 'left',
	38: 'up',
	// 39: 'right',
	40: 'down',
}

KEY_STATUS = {};
for (code in KEY_CODES) {
	KEY_STATUS[KEY_CODES[code]] = false;
}

document.onkeydown = function (e) {
	// Firefox and opera use charCode instead of keyCode to
	// return which key was pressed.
	var keyCode = (e.keyCode) ? e.keyCode : e.charCode;
	if (KEY_CODES[keyCode]) {
		e.preventDefault();
		KEY_STATUS[KEY_CODES[keyCode]] = true;
	}
}

document.onkeyup = function (e) {
	var keyCode = (e.keyCode) ? e.keyCode : e.charCode;
	if (KEY_CODES[keyCode]) {
		e.preventDefault();
		KEY_STATUS[KEY_CODES[keyCode]] = false;
	}
}

window.requestAnimationFrame = (function () {
	return window.requestAnimationFrame ||
		window.webkitRequestAnimationFrame ||
		window.mozRequestAnimationFrame ||
		window.oRequestAnimationFrame ||
		window.msRequestAnimationFrame ||
		function ( /* function */  callback, /* DOMElement */ element) {
			window.setTimeout(callback, 1000 / 60);
		};
})();

class Caroustack {
    constructor(params) {
        // params
        params = params || {};
        this.container = document.querySelector(params.container || '.container');
        this.items = document.querySelectorAll((params.container || '.container') + ' > ' + (params.items || '.item'));

        // transition variables
        this.currentSlide = 0;
        this.tempSlide = this.currentSlide;
        this.nextSlide = Math.min(this.currentSlide + 1, this.items.length - 1);
        this.delta = 0;
        this.angle = 0;

        // handlers
        this.initHandler = event => this.initScroll(event);
        this.moveHandler = event => this.moveScroll(event);
        this.endHandler = event => this.endScroll(event);

        // listeners
        this.container.addEventListener('pointerdown', this.initHandler);
        this.container.addEventListener('pointerup', this.endHandler);
        this.container.addEventListener('pointercancel', this.endHandler);

        // set item order
        this.items.forEach((i, index) => i.style.zIndex = -index);
        this.items[this.currentSlide].classList.add('active');
        this.items[this.nextSlide].classList.add('next');
    }

    initScroll(event) {
        // set initial values
        this.initialTouch = event.clientX;
        this.container.classList.add('sliding');
        this.container.addEventListener('pointermove', this.moveHandler);
    }

    moveScroll(event) {
        // transition values
        this.delta = this.initialTouch - event.clientX;
        this.angle = this.delta / 100;
        this.scaling = 1 - Math.abs(this.delta) / 5000;

        // set different slide if right or left
        let slide = this.tempSlide;
        this.tempSlide = this.delta < 0 ? Math.max(this.currentSlide - 1, 0) : this.currentSlide;

        // prevent spam slide stuck
        if (this.tempSlide !== slide) {
            this.items[slide].style.transform = `none`;
        }

        // update slide position
        this.items[this.tempSlide].style.transform = `translateX(${-this.delta}px) rotate(${-this.angle}deg) scale(${this.scaling})`;
    }

    endScroll(event) {
        // reset values
        this.container.removeEventListener('pointermove', this.moveHandler, false);
        this.container.classList.remove('sliding');
        this.items[this.tempSlide].style.transform = `none`;

        // you need to slide up to 50px to go prev/next
        if (Math.abs(this.delta) < 50) return;

        // reset items classes
        this.items.forEach(i => {
            i.classList.remove('active');
            i.classList.remove('next');
        });

        // set current slide
        this.currentSlide = this.delta > 0 ? this.tempSlide + 1 : this.tempSlide;
        if (this.currentSlide === this.items.length) {
            this.currentSlide = 0;
        }
        this.items[this.currentSlide].classList.add('active');

        // set next slide
        this.nextSlide = Math.min(this.currentSlide + 1, this.items.length - 1);
        this.items[this.nextSlide].classList.add('next');
    }

    getCurrentSlide() {
        return this.currentSlide;
    }
}
new Caroustack();

var c = new Caroustack();

function playClick() {
    const instruments = {
        1: "Piano",
        2: "Guitar",
        3: "Xylophone"
    }
    const instrument = instruments[this.c.currentSlide + 1];

    fetch(`http://localhost:5000/${instrument}`)
}

function stopPlaying() {
    fetch(`http://localhost:5000/stop`)
        .then(response => response.blob())
        .then(image => {
            var urlCreator = window.URL || window.webkitURL;
            var imageUrl = urlCreator.createObjectURL(image);
            console.log(imageUrl)
            document.getElementById("sheetMusic").src = imageUrl;
            document.getElementById("sheet").href = imageUrl
        });
}

$(function() {
    particlesJS("particles-js", {
        "particles": {
            "number": {
                "value": 80,
                "density": {
                    "enable": true,
                    "value_area": 800
                }
            },
            "color": {
                "value": "#812a8b"
            },
            "shape": {
                "type": "circle",
                "stroke": {
                    "width": 0,
                    "color": "#4d2851"
                },
                "polygon": {
                    "nb_sides": 5
                },
                "image": {
                    "src": "img/github.svg",
                    "width": 100,
                    "height": 100
                }
            },
            "opacity": {
                "value": 0.5,
                "random": false,
                "anim": {
                    "enable": false,
                    "speed": 1,
                    "opacity_min": 0.1,
                    "sync": false
                }
            },
            "size": {
                "value": 5,
                "random": true,
                "anim": {
                    "enable": false,
                    "speed": 40,
                    "size_min": 0.1,
                    "sync": false
                }
            },
            "line_linked": {
                "enable": true,
                "distance": 150,
                "color": "#ffffff",
                "opacity": 0.4,
                "width": 1
            },
            "move": {
                "enable": true,
                "speed": 4,
                "direction": "none",
                "random": false,
                "straight": false,
                "out_mode": "out",
                "bounce": false,
                "attract": {
                    "enable": false,
                    "rotateX": 600,
                    "rotateY": 1200
                }
            }
        },
        "interactivity": {
            "detect_on": "body",
            "events": {
                "onhover": {
                    "enable": true,
                    "mode": "repulse"
                },
                "onclick": {
                    "enable": true,
                    "mode": "push"
                },
                "resize": true
            },
            "modes": {
                "grab": {
                    "distance": 400,
                    "line_linked": {
                        "opacity": 1
                    }
                },
                "bubble": {
                    "distance": 400,
                    "size": 40,
                    "duration": 2,
                    "opacity": 4,
                    "speed": 3
                },
                "repulse": {
                    "distance": 200,
                    "duration": 0.4
                },
                "push": {
                    "particles_nb": 4
                },
                "remove": {
                    "particles_nb": 2
                }
            }
        },
        "retina_detect": true
    });
    var update;
    update = function() {
        if (window.pJSDom[0].pJS.particles && window.pJSDom[0].pJS.particles.array) {}
        requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
});
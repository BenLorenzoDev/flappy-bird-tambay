const canvas = document.getElementById('tetris');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');

const BOARD_WIDTH = 10;
const BOARD_HEIGHT = 20;
const BLOCK_SIZE = 30;

let board = Array(BOARD_HEIGHT).fill().map(() => Array(BOARD_WIDTH).fill(0));
let score = 0;
let dropTime = 0;
let lastTime = 0;

const tetrominoes = [
    {
        shape: [
            [1, 1, 1, 1]
        ],
        color: '#00f0f0'
    },
    {
        shape: [
            [1, 1, 1],
            [0, 1, 0]
        ],
        color: '#a000f0'
    },
    {
        shape: [
            [1, 1, 1],
            [1, 0, 0]
        ],
        color: '#f0a000'
    },
    {
        shape: [
            [1, 1, 1],
            [0, 0, 1]
        ],
        color: '#0000f0'
    },
    {
        shape: [
            [1, 1],
            [1, 1]
        ],
        color: '#f0f000'
    },
    {
        shape: [
            [1, 1, 0],
            [0, 1, 1]
        ],
        color: '#00f000'
    },
    {
        shape: [
            [0, 1, 1],
            [1, 1, 0]
        ],
        color: '#f00000'
    }
];

class Piece {
    constructor() {
        const randomTetromino = tetrominoes[Math.floor(Math.random() * tetrominoes.length)];
        this.shape = randomTetromino.shape;
        this.color = randomTetromino.color;
        this.x = Math.floor(BOARD_WIDTH / 2) - Math.floor(this.shape[0].length / 2);
        this.y = 0;
    }

    rotate() {
        const rotated = this.shape[0].map((_, index) =>
            this.shape.map(row => row[index]).reverse()
        );
        const backup = this.shape;
        this.shape = rotated;
        if (this.collides()) {
            this.shape = backup;
        }
    }

    move(dx, dy) {
        this.x += dx;
        this.y += dy;
        if (this.collides()) {
            this.x -= dx;
            this.y -= dy;
            return false;
        }
        return true;
    }

    collides() {
        for (let y = 0; y < this.shape.length; y++) {
            for (let x = 0; x < this.shape[y].length; x++) {
                if (this.shape[y][x] &&
                    (this.x + x < 0 ||
                     this.x + x >= BOARD_WIDTH ||
                     this.y + y >= BOARD_HEIGHT ||
                     board[this.y + y] && board[this.y + y][this.x + x])) {
                    return true;
                }
            }
        }
        return false;
    }

    lock() {
        for (let y = 0; y < this.shape.length; y++) {
            for (let x = 0; x < this.shape[y].length; x++) {
                if (this.shape[y][x]) {
                    if (this.y + y < 0) {
                        gameOver();
                        return;
                    }
                    board[this.y + y][this.x + x] = this.color;
                }
            }
        }
        clearLines();
        currentPiece = new Piece();
    }
}

let currentPiece = new Piece();

function clearLines() {
    let linesCleared = 0;
    for (let y = BOARD_HEIGHT - 1; y >= 0; y--) {
        if (board[y].every(cell => cell !== 0)) {
            board.splice(y, 1);
            board.unshift(Array(BOARD_WIDTH).fill(0));
            linesCleared++;
            y++;
        }
    }
    if (linesCleared > 0) {
        score += linesCleared * 100;
        scoreElement.textContent = score;
    }
}

function drawBlock(x, y, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
    ctx.strokeStyle = '#333';
    ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
}

function drawBoard() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    for (let y = 0; y < BOARD_HEIGHT; y++) {
        for (let x = 0; x < BOARD_WIDTH; x++) {
            if (board[y][x]) {
                drawBlock(x, y, board[y][x]);
            }
        }
    }
}

function drawPiece() {
    for (let y = 0; y < currentPiece.shape.length; y++) {
        for (let x = 0; x < currentPiece.shape[y].length; x++) {
            if (currentPiece.shape[y][x]) {
                drawBlock(currentPiece.x + x, currentPiece.y + y, currentPiece.color);
            }
        }
    }
}

function gameLoop(time = 0) {
    const deltaTime = time - lastTime;
    lastTime = time;
    dropTime += deltaTime;
    
    if (dropTime > 1000) {
        if (!currentPiece.move(0, 1)) {
            currentPiece.lock();
        }
        dropTime = 0;
    }
    
    drawBoard();
    drawPiece();
    requestAnimationFrame(gameLoop);
}

function gameOver() {
    alert('Game Over! Score: ' + score);
    board = Array(BOARD_HEIGHT).fill().map(() => Array(BOARD_WIDTH).fill(0));
    score = 0;
    scoreElement.textContent = score;
    currentPiece = new Piece();
}

document.addEventListener('keydown', (e) => {
    switch(e.key) {
        case 'ArrowLeft':
            currentPiece.move(-1, 0);
            break;
        case 'ArrowRight':
            currentPiece.move(1, 0);
            break;
        case 'ArrowDown':
            currentPiece.move(0, 1);
            break;
        case 'ArrowUp':
            currentPiece.rotate();
            break;
        case ' ':
            e.preventDefault();
            while (currentPiece.move(0, 1)) {}
            currentPiece.lock();
            break;
    }
});

gameLoop();
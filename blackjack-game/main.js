class Configuration {
  constructor(decks, cutEnabled, showHandValue, tableMinimum) {
    this.decks = decks;
    this.cutEnabled = cutEnabled;
    if (this.cutEnabled === true && this.decks > 1) this.cutPos = getRandomCut(decks);
    else this.cutPos = decks*52;
    this.betUnit = 1;
    this.showHandValue = showHandValue;
    this.tableMinimum = tableMinimum;
  }
}

const config = new Configuration(8, true, true, 5); // Set configuration here
let bankroll = 1000; // Set starting bankroll here
const logEnabled = true; // Enable log
const clearConsole = true; // Clear the console time

const values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
const suits = ['C', 'D', 'H', 'S'];
const deck = shuffleDeck(buildDeck());

/* const deck = [

    "2-C", "4-D",    
    "2-D", "6-S",    
    "10-C", "10-H",    


    "J-S", "6-C",
    "Q-D", "8-H",
    "2-H", "A-C",


    "5-S", "9-D",
    "5-H", "7-S",
    "4-D", "2-S",

    "2-C", "J-H",
    "9-S", "5-C",


    "9-H", "4-D",
    "9-C", "3-S",
    "6-H", "Q-D",

    "A-S", "10-H",
    "A-D", "2-D",
    "8-C", "7-H",

    "3-H", "K-D",
    "3-D", "6-S",
    "7-D", "4-C",

    "2-C", "5-H",
    "J-D", "6-H",
    "K-C", "10-C",
] */

const discards = []

const playerHands = [[]];
let playerHandIdx = 0;

const dealerHand = [];

let bet = 0;
let totalGain = 0;
let lastHandGain = 0;
let resultHTML = '';

let chip1Count = 0;
let chip2Count = 0;
let chip3Count = 0;
let chip4Count = 0;

let splitCount = 0;


// const deck = ['10-S',  '5-D', 'A-D', '6-H',  '10-D', '10-D', '2-S', '2-H', '2-D', '2-D', '2-S', '2-H', '2-D', '2-D', '2-S', '2-H',
//   '2-D', '2-D', '2-S', '2-H', '2-D', '3-D', '2-S', '8-H', '2-D', '3-D', '2-S', '8-H', '2-D', '3-D', '2-S', '8-H'
// ]


// Gut deck cut at random position in range (deckSize/2, deckSize - "half a deck")
function getRandomCut(decks) {
  const cardNum = decks*52;
  const min = Math.ceil(cardNum/2);
  const max = Math.floor(cardNum - 26);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getPlayerHandsTotalCardNum()
{
  let total = 0;
  for (const hand of playerHands)
    total += hand.length;
  return total;
}

// Function to log important things
function logDebug() {
  if (logEnabled === true) {
    if (clearConsole)
      console.clear();
    console.log("player");
    console.log(playerHands);
    console.log("dealer");
    console.log(dealerHand);
    console.log("deck"); 
    console.log(deck);
    console.log("discards"); 
    console.log(discards);
    console.log("cut pos"); 
    console.log(config.cutPos);
    console.log("discards len");
    console.log((discards.length));
    console.log("table cards");
    let playerHandsTotalCards = getPlayerHandsTotalCardNum();
    console.log((playerHandsTotalCards + dealerHand.length));
    console.log("total gain");
    console.log(totalGain);
    console.log("split count");
    console.log(splitCount)
  }
}

// Function to sleep for a while ms
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Function to create a single deck of cards
function buildDeck() {
  const deck = [];
  for (let i = 0; i < config.decks; i++) {
    for (const value of values) {
      for (const suit of suits) {
        deck.push(`${value}-${suit}`);
      }
    }
  }
  return deck;
}

// Function to shuffle the deck of cards
function shuffleDeck(deck) {
  for (let i = deck.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [deck[i], deck[j]] = [deck[j], deck[i]];
  }
  return deck;
}

// Refill the deck using discads
function addDiscardsToDeck() {
  shuffleDiscards = shuffleDeck(discards);
  
  for (const card of shuffleDiscards)
    deck.push(card);
  discards.length = 0;

  if(this.cutEnabled === true && this.decks > 1)
    config.cutPos = getRandomCut(config.decks);
}

// Add discards if deck is empty or reached the cut (if enabled in configuration)
function checkDeck() {
  let playerHandsTotalCards = getPlayerHandsTotalCardNum();

  if ((discards.length + playerHandsTotalCards + dealerHand.length) === config.cutPos)
    addDiscardsToDeck();
}

// Put hand in discard
function putToDiscardPile(hand) {
  for (const card of hand)
    discards.push(card);
}

function checkSameValue(card1, card2)
{
  const card1Value = card1.split('-')[0];
  const card2Value = card2.split('-')[0];

  if (card1Value === card2Value)
    return true;
  else if (['10', 'J', 'Q', 'K'].includes(card1Value) && ['10', 'J', 'Q', 'K'].includes(card2Value))
    return true;

  return false;
}

// Function to deal cards to the player and dealer
function dealCards(deck, playerHand, dealerHand) {
  if (bet < config.tableMinimum) {
    alert("You must place at least the table minimum to play.");
    return;
  }

  document.querySelector('.js-result').innerHTML = "Game";

  document.querySelector('.js-play-button').style.display = 'none';
  document.querySelector('.js-bet1-button').style.display = 'none';
  document.querySelector('.js-bet2-button').style.display = 'none';
  document.querySelector('.js-bet3-button').style.display = 'none';
  document.querySelector('.js-bet4-button').style.display = 'none';


  document.querySelector('.js-hit-button').style.display = 'inline-block';
  document.querySelector('.js-stand-button').style.display = 'inline-block';
  document.querySelector('.js-strategy-button').style.display = 'inline-block';

  //updateGameData();

  playerHand.length = 0;
  dealerHand.length = 0;
  for (let i = 0; i < 2; i++) {
    checkDeck();
    playerHand.push(deck.shift());

    checkDeck();
    dealerHand.push(deck.shift());
  }

  // Show double button if have to
  if (playerHand.length === 2) {
    if ((calculateHandTotal(playerHand) >= 9) && (calculateHandTotal(playerHand) <= 11)) {
      if ((bet*2) <= bankroll) {
        document.querySelector('.js-double-button').style.display = 'inline-block';
      }
    }
  }

  if (playerHand.length === 2 && splitCount < 3 && checkSameValue(playerHand[0], playerHand[1]))
  {
    document.querySelector('.js-split-button').style.display = 'inline-block';
  }

  updateDOM();
  updateGameData();

  logDebug(); // log data to debug purpose

  // Enable buttons
  enableButtons();
}

// Function to update the DOM with player and dealer cards
function updateDOM() {

  for (let i = 0; i < playerHands.length; i++) {
    if (i === playerHandIdx && splitCount > 0) {
      document.querySelector(`.js-player-hand-${i}`).style.padding = '0.5rem'
      document.querySelector(`.js-player-hand-${i}`).style.backgroundColor = 'rgb(20, 83, 45)';

        playerCurrHand = playerHands[playerHandIdx];
        if (playerCurrHand.length === 2 && splitCount < 3 && checkSameValue(playerCurrHand[0], playerCurrHand[1]))
        {
          document.querySelector('.js-split-button').style.display = 'inline-block';
        }
    }
    else {
      document.querySelector(`.js-player-hand-${i}`).style.padding = '0rem'
      document.querySelector(`.js-player-hand-${i}`).style.backgroundColor = 'rgb(22, 101, 52)';
    }

    if (splitCount > 1 && playerHands[0][0].split('-')[0] != 'A')
    {
      document.querySelector(`.js-player-hand-${i}`).style.display = "block";
    }
    else {
      document.querySelector(`.js-player-hand-${i}`).style.display = "inline-block";
    }

    document.querySelector(`.js-player-cards-${i}`).style.display = "flex";
    document.querySelector(`.js-name-header-${i}`).style.display = "block"

    document.querySelector(`.js-player-cards-${i}`).innerHTML = playerHands[i].map(card => `
      <img class="playing-card" src="./images/cards/${card}.png" alt="Image of a playing card">
    `).join('');

    if (config.showHandValue)
      document.querySelector(`.js-player-score-${i}`).innerHTML = calculateHandTotal(playerHands[i]);
  }

  document.querySelector('.js-dealer-cards').innerHTML = `
    <img class="playing-card card-back" src="./images/cards/BACK.png" alt="Image of a playing card face down">
    <img class="playing-card" src="./images/cards/${dealerHand[0]}.png" alt="Image of a playing card face up">
  `;

  if (config.showHandValue)
    document.querySelector('.js-dealer-score').innerHTML = calculateHandTotal(dealerHand.slice(0, 1));
}

// Function to calculate the total value of a hand
function calculateHandTotal(hand) {
  let total = 0;
  let aces = 0;

  for (const card of hand) {
    const value = card.split('-')[0];
    if (value === 'A') {
      aces += 1;
      total += 11;
    } else if (['J', 'Q', 'K'].includes(value)) {
      total += 10;
    } else {
      total += parseInt(value);
    }
  }

  while (total > 21 && aces > 0) {
    total -= 10;
    aces -= 1;
  }
  
  return total;
}

// Function to handle the hit button
function hit(deck, playerHand) {
  disableButtons();
  document.querySelector('.js-split-button').style.display = 'none';
  document.querySelector('.js-double-button').style.display = 'none';

  checkDeck();
  playerHand.push(deck.shift());
  updateDOM();
  updateGameData();
  const total = calculateHandTotal(playerHand);
  if (total > 21) {
    document.querySelector('.js-result').innerHTML = 'Player Busted!';
    //stand(deck, dealerHand);
    if (playerHands.length === (playerHandIdx + 1)) {
      // for (let i = 0; i < playerHands.length; i++)
      //   determineWinner(playerHands[i], dealerHand);
      if (playerHands.length === 1) {
        determineWinner(playerHand, dealerHand);
      }
      else {
        let bustedAll = true;
        for (const hand of playerHands) {
          if (calculateHandTotal(hand) < 22)
            bustedAll = false;
        }

        if (bustedAll === false) {
          stand(deck, dealerHand);
        }
        else {
          for (const hand of playerHands) {
            determineWinner(hand, dealerHand);
          }
        }
      }
    }
    else {
      playerHandIdx += 1;
      updateDOM();
      enableButtons();
    }
  }
  else {
    enableButtons();
  }
}

// Function to handle the stand button and start the dealer's turn
async function stand(deck, dealerHand) {
  disableButtons();
  document.querySelector('.js-split-button').style.display = 'none';
  document.querySelector('.js-double-button').style.display = 'none';

  if (playerHands.length === (playerHandIdx + 1)) {

    document.querySelector('.js-dealer-cards').innerHTML = dealerHand.map(card => `
      <img class="playing-card" src="./images/cards/${card}.png" alt="Image of a playing card">
    `).join('');

    if (config.showHandValue)
      document.querySelector('.js-dealer-score').innerHTML = calculateHandTotal(dealerHand);

    await sleep(1000); // sleep 1 sec

    while (calculateHandTotal(dealerHand) < 17) {
      checkDeck()
      dealerHand.push(deck.shift());
      updateGameData();

      document.querySelector('.js-dealer-cards').innerHTML += `
        <img class="playing-card" src="./images/cards/${dealerHand[dealerHand.length - 1]}.png" alt="Image of a playing card">
      `;

      if (config.showHandValue)
        document.querySelector('.js-dealer-score').innerHTML = calculateHandTotal(dealerHand);

      await sleep(1000); // sleep 1 sec
      
    }

    for (let i = 0; i < playerHands.length; i++)
      determineWinner(playerHands[i], dealerHand);
  }
  else {
    playerHandIdx += 1;
    enableButtons();
    updateDOM();
  }
  
}

// Function to disable the hit and stand buttons
function disableButtons() {
  document.querySelector('.js-hit-button').disabled = true;
  document.querySelector('.js-stand-button').disabled = true;
}

// Function to enable the hit and stand buttons
function enableButtons() {
  document.querySelector('.js-hit-button').disabled = false;
  document.querySelector('.js-stand-button').disabled = false;
}


// Function to determine the winner of the game
function determineWinner(playerHand, dealerHand) {
  disableButtons(); // Disable the buttons when the deal is over

  document.querySelector('.js-dealer-cards').innerHTML = dealerHand.map(card => `
  <img class="playing-card" src="./images/cards/${card}.png" alt="Image of a playing card">
  `).join('');

  const playerTotal = calculateHandTotal(playerHand);
  const dealerTotal = calculateHandTotal(dealerHand);
  
  document.querySelector('.js-dealer-score').innerHTML = dealerTotal

  if (playerTotal > 21) {
    resultHTML += 'You Lose';
    totalGain -= bet;
    lastHandGain -= bet;
    bankroll -= bet;
  }
  else if (dealerTotal > 21 || playerTotal > dealerTotal) {
    if ((playerTotal === 21) && (playerHand.length === 2) && (splitCount === 0)) {
      resultHTML += 'Blackjack!';
      let halfBet = bet/2;
      totalGain += bet;
      totalGain += halfBet
      lastHandGain += bet;
      lastHandGain += halfBet
      bankroll += bet;
      bankroll += halfBet;
    } 
    else {
      resultHTML += 'Player Wins';
      totalGain += bet;
      lastHandGain += bet;
      bankroll += bet;
    }
  }
  else if (playerTotal < dealerTotal) {
    resultHTML += 'Dealer Wins';
    totalGain -= bet;
    lastHandGain -= bet;
    bankroll -= bet;
  }
  else {
    if (playerTotal === 21 && dealerTotal === 21)
    {
      if (splitCount === 0 && playerHand.length === 2 && dealerHand.length > 2)
      {
        resultHTML += 'Blackjack!';
        let halfBet = bet/2;
        totalGain += bet;
        totalGain += halfBet
        lastHandGain += bet;
        lastHandGain += halfBet
        bankroll += bet;
        bankroll += halfBet;
      }
      else if (dealerHand.length === 2 && playerHand.length > 2) {
        resultHTML += 'Dealer Wins';
        totalGain -= bet;
        lastHandGain -= bet;
        bankroll -= bet;  
      }
      else {
        resultHTML += 'Push';
        lastHandGain += 0;        
      }
    }
    else {
      resultHTML += 'Push';
      lastHandGain += 0;
    }
  }

  if (splitCount > 0 && (playerHand != playerHands[playerHands.length-1])) {
    resultHTML += ' | '
  }

  document.querySelector('.js-result').innerHTML = resultHTML;

  if (playerHands.length === (playerHandIdx + 1)) {
    document.querySelector('.js-new-game-button').style.display = 'inline-block';
  }

  updateGameData();
  document.querySelector('.js-last-hand-gain').innerHTML = `<p>${lastHandGain} bu</p>`;

  logDebug(); // log data to debug purpose
}

// update bet container
function updateBetOnScreen() {
  document.querySelector('.js-bet').innerHTML = `<p>${bet} bu</p>`;
}

// Add a bet unit
function addToBet(nbu)
{
  if ((bet + nbu) > bankroll) {
    alert("You don't have enough money!")
    return false;
  }
  bet += nbu;
  updateBetOnScreen()
  return true;
}

function addBetUnitChip1() {
  if(addToBet(config.betUnit) === true) {
    chip1Count += 1;
  }
  document.querySelector('.js-bet1-button').innerHTML = `
    x${chip1Count}<img src="images/chips/chipBlackWhite.png" alt="Bet button" class="bet-button-img">`;
}

function addBetUnitChip2() {
  if(addToBet(config.betUnit*5) === true) {
    chip2Count += 1;
  }
  document.querySelector('.js-bet2-button').innerHTML = `
    x${chip2Count}<img src="images/chips/chipBlueWhite.png" alt="Bet button" class="bet-button-img">`;
}

function addBetUnitChip3() {
  if(addToBet(config.betUnit*10) === true) {
    chip3Count += 1;
  }
  document.querySelector('.js-bet3-button').innerHTML = `
    x${chip3Count}<img src="images/chips/chipGreenWhite.png" alt="Bet button" class="bet-button-img">`;
}

function addBetUnitChip4() {
  if(addToBet(config.betUnit*25) === true) {
    chip4Count += 1;
  }
  document.querySelector('.js-bet4-button').innerHTML = `
    x${chip4Count}<img src="images/chips/chipRedWhite.png" alt="Bet button" class="bet-button-img">`;
}


// Reset bet unit
function resetBet() {
  bet = 0;
  chip1Count = 0;
  chip2Count = 0;
  chip3Count = 0;
  chip4Count = 0;
  document.querySelector('.js-bet1-button').innerHTML = `
    x${chip1Count}<img src="images/chips/chipBlackWhite.png" alt="Bet button" class="bet-button-img">`;
  document.querySelector('.js-bet2-button').innerHTML = `
    x${chip2Count}<img src="images/chips/chipBlueWhite.png" alt="Bet button" class="bet-button-img">`;
  document.querySelector('.js-bet3-button').innerHTML = `
    x${chip3Count}<img src="images/chips/chipGreenWhite.png" alt="Bet button" class="bet-button-img">`;
  document.querySelector('.js-bet4-button').innerHTML = `
    x${chip4Count}<img src="images/chips/chipRedWhite.png" alt="Bet button" class="bet-button-img">`;
}

// double button function
function double() {
  disableButtons();
  if (addToBet(bet) === true) {
    document.querySelector('.js-double-button').style.display = 'none';
    document.querySelector('.js-split-button').style.display = 'none';
    hit(deck, playerHands[playerHandIdx]);
    if (calculateHandTotal(playerHands[playerHandIdx]) <= 21) { // check player did not already busted
      stand(deck, dealerHand);
    }
  }
  else {
    enableButtons();
  }
}

async function split() {
  disableButtons();
  if (((bet*(splitCount + 1)) + bet) <= bankroll) {

    document.querySelector('.js-split-button').style.display = 'none';
    document.querySelector('.js-double-button').style.display = 'none';

    splitCount += 1;

    // Split current hand creating a new one in the end of player hand array
    cardToSplit = playerHands[playerHandIdx].pop();
    const cardValue = cardToSplit.split('-')[0];

    if (cardValue === 'A') { 
      splitCount = 3; // If you split aces you can do it only one time
      document.querySelector('.js-hit-button').style.display = 'none'; // You cannot do hit anymore
      document.querySelector('.js-stand-button').style.display = 'none'; // unusefull
    }

    checkDeck();
    playerHands[playerHandIdx].push(deck.shift())
    checkDeck();
    playerHands.push([cardToSplit, deck.shift()]);
    updateDOM();
    updateGameData();

    if(cardValue === 'A') {
      await sleep(1000);
      stand(deck, dealerHand);
      await sleep(1000);
      stand(deck, dealerHand);
    }
  }
  else {
    alert(`You don't have enough money to split ${splitCount + 1} times!`);
  }

  enableButtons();
}

function roundDecks(cardNum) {
  const decksNum = cardNum / 52;
  return Math.round(decksNum * 2) / 2;
}

// Update side game data
function updateGameData() {
  document.querySelector('.js-decks-num').innerHTML = `<p>${config.decks}</p>`;
  document.querySelector('.js-remaining-cards').innerHTML = `<p>${deck.length} (<i>Decks:</i> ${roundDecks(deck.length)})</p>`;
  document.querySelector('.js-discard-pile-cards').innerHTML = `<p>${discards.length} (<i>Decks:</i> ${roundDecks(discards.length)})</p>`;
  document.querySelector('.js-cut-pos').innerHTML = `<p>${config.cutPos}</p>`;
  document.querySelector('.js-total-gain').innerHTML = `<p>${totalGain} bu</p>`;
  // document.querySelector('.js-last-hand-gain').innerHTML = `<p>${lastHandGain} bu</p>`;
  document.querySelector('.js-bankroll').innerHTML = `<p>${bankroll} bu</p>`;
  document.querySelector('.js-table-minimum').innerHTML = config.tableMinimum;
}

// Event listeners
document.querySelector('.js-hit-button').addEventListener('click', () => hit(deck, playerHands[playerHandIdx]));
document.querySelector('.js-stand-button').addEventListener('click', () => stand(deck, dealerHand));
document.querySelector('.js-play-button').addEventListener('click', () => dealCards(deck, playerHands[playerHandIdx], dealerHand));
document.querySelector('.js-new-game-button').addEventListener('click', () => showFaceDownCards());
document.querySelector('.js-strategy-button').addEventListener('click', () => {
  document.querySelector('.js-strategy-div').classList.toggle('hidden');
});
document.querySelector('.js-strategy-div').addEventListener('click', () => {
  document.querySelector('.js-strategy-div').classList.toggle('hidden');
});
document.querySelector('.js-bet1-button').addEventListener('click', () => addBetUnitChip1());
document.querySelector('.js-bet2-button').addEventListener('click', () => addBetUnitChip2());
document.querySelector('.js-bet3-button').addEventListener('click', () => addBetUnitChip3());
document.querySelector('.js-bet4-button').addEventListener('click', () => addBetUnitChip4());
document.querySelector('.js-double-button').addEventListener('click', () => double());
document.querySelector('.js-split-button').addEventListener('click', () => split());

// Show face down cards
function showFaceDownCards() {
  document.querySelector('.js-result').innerHTML = "Do your bet!";

  putToDiscardPile(dealerHand);
  
  for (const hand of playerHands) {
      putToDiscardPile(hand);
  }

  updateGameData();
  resetBet();
  updateBetOnScreen();

  for (let i = 1; i < playerHands.length; i++) {
    document.querySelector(`.js-player-hand-${i}`).style.display = 'none'
    // document.querySelector(`.js-player-cards-${i}`).style.display = "none";
  }

  resultHTML = "";
  lastHandGain = 0;

  playerHands.length = 1;
  playerHandIdx = 0;
  playerHands[playerHandIdx] = [];
  splitCount = 0;

  document.querySelector('.js-name-header-0').style.display = "block";
  document.querySelector('.js-player-cards-0').style.display = "flex";

  if (config.showHandValue) {
    document.querySelector('.js-player-score-0').innerHTML = 0;
    document.querySelector('.js-dealer-score').innerHTML = 0;
  }
  
  document.querySelector('.js-dealer-cards').innerHTML = `
    <img class="playing-card card-back" src="./images/cards/BACK.png" alt="Image of a playing card face down">
    <img class="playing-card card-back" src="./images/cards/BACK.png" alt="Image of a playing card face down">
  `;
  document.querySelector('.js-player-cards-0').innerHTML = `
    <img class="playing-card card-back" src="./images/cards/BACK.png" alt="Image of a playing card face down">
    <img class="playing-card card-back" src="./images/cards/BACK.png" alt="Image of a playing card face down">
  `;

  document.querySelector('.js-play-button').style.display = 'inline-block';
  document.querySelector('.js-bet1-button').style.display = 'inline-block';
  document.querySelector('.js-bet2-button').style.display = 'inline-block';
  document.querySelector('.js-bet3-button').style.display = 'inline-block';
  document.querySelector('.js-bet4-button').style.display = 'inline-block';

  document.querySelector('.js-hit-button').style.display = 'none';
  document.querySelector('.js-stand-button').style.display = 'none';
  document.querySelector('.js-double-button').style.display = 'none';
  document.querySelector('.js-split-button').style.display = 'none';
  document.querySelector('.js-strategy-button').style.display = 'none';
  document.querySelector('.js-new-game-button').style.display = 'none';
}


// Initial deal
//dealCards(deck, playerHand, dealerHand);
showFaceDownCards();
logDebug();

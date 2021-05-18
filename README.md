# Solving the Cryptid boardgame

A solver for the boardgame [Cryptid](https://ospreypublishing.com/store/osprey-games/board-card-games/cryptid?___store=osprey_rst). Currently this solver supports interactive mode (Helping to find good moves), but extending it to simulated games should not be too much trouble. With simulated games different gameplay styles could be analysed and compared (e.g. accounting for unknown information in decision making).

## Running the solver in interactive mode

Start by installing the package.
In the project folder run:

```
pip install .
```

Invoke the interactive solver with help menu:

```
python interactive_solver.py -h
```

## Development principles

This 'solver' is expected to require simulated games to find close to optimal strategies. Thus:

1. As the number of required simulations can become numerous, following choices are attempted to encourage.
    1. Mutable states are avoided - to allow easy parallel branching
    2. Use set operations - inexpensive and fitting for the gameplay
2. Attempt to use class structures that easy to grasp
3. Attempt to use polymorphism, and small set of functions. Following ['Simple Made Easy'](https://www.infoq.com/presentations/Simple-Made-Easy) talk

## Milestones

* 17.5.2021: Solver's first win against a human 🥳

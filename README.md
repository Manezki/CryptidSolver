# Solving the Cryptid boardgame

## Development principles

This 'solver' is expected to require simulated games to find optimal strategies. As the state-space is not overwhelming, I see this as a nice opportunity to consider Alpha-Go like solutions. Thus:

1. The simulations of the game needs to be scalable
    1. Mutable states are avoided - to allow easy parallel branching
    2. Use set operations - inexpensive and fitting for the gameplay
2. Attempt to use class structures that easy to grasp
3. Attempt to use polymorphism, and small set of functions. Following ['Simple Made Easy'](https://www.infoq.com/presentations/Simple-Made-Easy) talk
# Persian Ney csp solver

If you don't know what Persian Ney (one of the oldest musical instruments still in use) is and how it is traditionally constructed, please read [this website](https://www.persianney.com/) and this [Wikipedia article](https://en.wikipedia.org/wiki/Ney).

As part of a research on constructing Persian Ney reliably, accurately, and efficiently, this CSP solver acts as a design-aid tool.
The problem of designing and constructing this woodwind instrument, after some studies on Physics and music theory as well as a few informal experiments, 
led to the invention of a relatively new technique.

In this new technique, the instrument is built with [natural canes](https://en.wikipedia.org/wiki/Arundo_donax) extracted from [canebrakes](https://en.wikipedia.org/wiki/Canebrake), cut at their nodes junctions, 
mix and match the pieces, stick them together, and build holes on the final pipe.

This tool helps in the mix-and-match part, which turns out to be a combinatorial search problem. Based on advises from professional Ney constructors and 
players, a few characteristics including the shape of the final pipe, the relationship between length of nodes, and etc have been incorporated into
several unary, binary, and higher level constraints.

Based on the nature of constraints, efficient algorithms were found to establish binary and n-ary consistency. Hence, the sover does not use algorithms like
arc3, and instead conducts the search by maintaining the domains consistent, reducing the search space significantly. Some domains are defined as ranges of integer values and some are defined as a set of values.

Furthermore, the solver adops conflict-directed [backjumping](https://en.wikipedia.org/wiki/Backjumping). In the final phase of the project, constraint learning will be added to make constructing different sound registers efficient and fast.

**This is still a work in progress and a paper explaining the details will be authored.**

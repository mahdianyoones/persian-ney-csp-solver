# Persian Ney csp solver

Persian Ney is one of the oldest musical instruments still in use. For more information  read [this website](https://www.persianney.com/) and this [Wikipedia article](https://en.wikipedia.org/wiki/Ney).

This instrument is extremely simple, having a pipe-like structure. Traditionally, the constructors of this instrument look for natural canes in a [canebrakes](https://en.wikipedia.org/wiki/Canebrake) that has certain length, given the frequency range they need to obtain from it. Larger instruments--sound pipes--produce lower frequencies and smaller ones producer higher ones.

The length of the pipe is not the only factor to make a Ney useful. Certain elationships must exist between its nodes, according to Masters of this instrument--more impotantly Mr Kianinejad. The length of the nodes must decrease in an orderly fashion. That is, starting from top, subsequent nodes must keep decreasing in length. Further, it is better for the nodes to keep decreasing in diameter, too. Which would make the final pipe a cone.

While there a lot of quality instrumns are produced, instruments that have all these properties are rare. That is in part due to the random growing nature of the plant. In a canebrake, probably a few branches would exibit these desirable properties naturally.

Given that after cutting the promising branches, they need to be stored for a couple of months, at least, for drainage, the construction becomes a risky process. This problem has led to scarcity of quality instruments.

One solution is not using natural canes and instead using other materials, such as wood. This idea has led to successful alternative construction methods. However, among the community of Nay players and masters, Neys constructed via natural canes are more favorable.

The solution that is proposed in this study consist of using [natural canes](https://en.wikipedia.org/wiki/Arundo_donax) and reconfiguring the nodes. That is, instead of limiting oneself to the limited imperfect variety offered by the nature, a constructor can take any number of branches, cut its nodes, and reconfigure them to build perfect structures. The nodes can be connected again using proper stick, which is out of the scope of this paper.

This project devlops a CSP-solver that acts as a design-aid tool hepling with the mix-and-match part, which turns out to be a combinatorial search problem, suitable for modeling as a [Constraint Satisfaction Problem](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem). 

The desirable relationsships between nodes mentioned above have been incorporated into
several unary, binary, and higher level constraints in the CSP model.

Based on the nature of constraints, efficient algorithms were found to establish binary and n-ary consistency. Hence, the sover does not use algorithms like
arc3, and instead conducts the search by maintaining the domains consistent, reducing the search space significantly. Some domains are defined as ranges of integer values and some are defined as a set of values.

Furthermore, the solver adops conflict-directed [backjumping](https://en.wikipedia.org/wiki/Backjumping). In the final phase of the project, constraint learning will be added to make constructing different sound registers efficient and fast.

Another part this problem tries to solve is not only finding the nodes that can go together to build a single instrument, but given a stock of pieces at hand, making any possible number of instruments that are feasible.

That is, imagine a Ney constructor has cut several cane branches from a canebrake and wants to build some instruments out of them. They cut all the branches into pieces at their junctions. Then, they try to figure out the maximum number of instruments that the stock can yield.

The number of instruments, however, is not the only quantity, a construcor would maximize. Instruments with certain length are more common, given the frequency range they can produce. For example, instruments that produce Bb or C are much more common. Therefore, the optimization part needs to take this into account as well as the fact that if a player has a varied collection of instruments, they can virtually play any melody.

Therefore, the objective of this research is not only making a single instrument with some cut pieces, but also making the most out of them in favor of the player.

**The project has achieved all the aims mentioned above; however, when the pieces are large and varied--input of the algorith, the algorithm does not terminate. It sounds like this is an NP problem. That is, the time complexity grows exponentially.**
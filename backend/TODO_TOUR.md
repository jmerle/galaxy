# Tournament thoughtdump

## Principles

- Ease of management
- As much automated as possible
- ideally just hit the admin panel for all the things
- Use challonge as much as possible to do bracket stuffs. pls no reinvent wheel T_T

## Code outline

- user creates a tour, with blank challonge links, and "in progress" is false
- user presses a button on admin panel to "initialize" it
- Backend finds that this tour has blank challonge links yet "in progress", and initializes it:
  - Creates 1 new tournament, **private** https://api.challonge.com/v1/documents/tournaments/create
  - Adds the participants to challonge
    - Derive them via eligibility criteria
    - Put them to challonge via https://api.challonge.com/v1/documents/participants/bulk_add
  - Adds rounds (at least w partial info? idk) to BC backend
    - Make sure rounds have descriptive names, eg "tourname-r1-winners" or smth
    - So this is hard, cuz rounds aren't directly exposed by challonge API. Perhaps best is to get the matchlist (https://api.challonge.com/v1/documents/matches/index) and then iterate through all of them and find distinct rounds.
    - For double elim, challonge API numbers rounds really strangely. We can deal with it tho; just need some manual labor
- User assigns maps to those rounds via admin panel
  - IDK, this seems likes the best way to set maps, without high effort. Yay admin panel! Also this order guarantees that
- User clicks some button to begin. Perhaps switch the backend tour to "in progress" here

Periodically (how? via scheduler? while loop? etc...see below)

- Backend hits challonge map list
- For each api match whose state (on api) is "open"...
  - (TODO NEED TO ENSURE THAT MULTIPLE BACKENDS DONT ACT ON SAME MATCH)
  - Create match in backend db. Associate it with the proper tour and tour round!!!
  - Send match to be run by saturn, via pubsub
- For each match in backend db that is associated with a relevant tour round, and which is completed:
  - Report it to challonge via api (https://api.challonge.com/v1/documents/matches/update)
- For each match as above that tried to run but failed cuz Saturn
  - Ask to retry
- Rinse wash repeat til tour is done

Then the next step ...

- Create a public bracket on challonge.
- As matches are streamed (or pre-released), publish matches/rounds to that challonge bracket.
  - Is easiest via some bulk buttons on admin interface. I think this needs to be impld.

After stream...

- Change tour things to allow tour matches to be shown in dashboard

TODO I'm missing some details about round visibility on backend server

## Architecture Concerns

- "In progress?" isn't as robust as I'd like. maybe need an enum of a few things

  - uninitialized / initialized / in progress / etc

- Many backend servers exist and run, hence concurrency issues etc
- If done stupidly, backend server could be frozen in a sad while loop
- Scheduler to auto-start tournaments?
- Scheduler to auto-query an endpoint, to keep the tournament running?

## Work concerns

- Nathan knows how to do all the challonge stuff; it's kinda c-p from years prior.
- Nathan does not know our backend code well enough. He can struggle through it, but might be better to get a hard carry from someone else. Esp for design decisions.

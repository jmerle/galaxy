# Tournament thoughtdump

## Principles

- Ease of management
- As much automated as possible
- ideally just hit the admin panel for all the things
- Use challonge as much as possible to do bracket stuffs. pls no reinvent wheel T_T

## Code TODOs

- Backend finds that this tour has blank challonge links yet "in progress", and initializes it:
  - Adds the participants to challonge
    - Derive them via eligibility criteria properly
  - Adds rounds to BC backend
    - For double elim, challonge API numbers rounds really strangely. We can deal with it tho; just need some manual labor

Periodically (how? via scheduler? while loop? etc...see below)

- User asks for a round to be done:
  - Backend hits challonge match list
  - For each api match whose state (on api) is "open"...
    - Create match in backend db. Associate it with the proper tour and tour round!!!
    - Send match to be run by saturn, via pubsub
  - For each match in backend db that is associated with a relevant tour round, and which is completed:
    - Report it to challonge via api (https://api.challonge.com/v1/documents/matches/update)
  - For each match as above that tried to run but is declared as Error by Saturn..
    - Re-run the entire round. (later it'd be nice to re-run just a match but)
- If needed, user can bulk restart a round
  - Clear round and any future dependencies
- Rinse wash repeat til tour is done
- Create the tour-result json expected by client, and provide to admin (how?)

Then the next step ...

- Create a public bracket on challonge.
- As matches are streamed (or pre-released), publish matches/rounds to that challonge bracket.
  - Is easiest via some bulk buttons on admin interface. See backend/siarnaq/api/episodes/models.py / TournamentRound.release_status, which will release in bulk by round

After stream...

- Change tour things to allow tour matches to be shown in dashboard

## GitHub / Code Ops TODOs

- TEST TEST TEST
- Finalize and create back-\_in_compatible migrations, and release them on staging (and in prod later)
- File a new issue for double-elim tours (and other refinements)
- Port this TODO doc into GH issues
- A fun TODO is to run everything all in one go, ie not have to wait round-by-round. This takes care for concurrency issues / queueing the same match multiple times.
  - The best idea would be to, when a match is done, query for matches that are newly "open" and have not yet been already entered in DB and fired off to scrim servers. But, you'd have to make sure that two servers don't see the same newly open things and queue them both. Perhaps this is work-aroundable via locking.

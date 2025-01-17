# Codebase Intro and Guide

**If you are trying to make code changes here, make sure to read all the (sub)sections called "Technical Detail".** _If you're not trying to make code changes but just need some working knowledge, then feel free to skip over those sections._ It's helpful but not necessary.

The intent of this page is to discuss technical parts just enough, to get people started or reduce confusion. Feel free to change this and add more detail as it might be helpful (although it should probably go into other pages).

## Web Programming knowledge

General principles and packages of web programming, that Battlecode uses.

### NPM

NPM, the Node Package Manager, is an online repository of JS packages, and a way to download and use them. It also exposes some helpful utilities.

To run the frontend locally, you'll need to install the NPM CLI (command-line interface). See `local-setup.md` for more.

and then react-scripts

#### Technical Detail

Here's a good tutorial to NPM, that should give you all you need. (It might actually give too much detail -- feel free to strip down as necessary.) [https://www.freecodecamp.org/news/what-is-npm-a-node-package-manager-tutorial-for-beginners/](https://www.freecodecamp.org/news/what-is-npm-a-node-package-manager-tutorial-for-beginners/)

If this ever goes down or you don't like this tutorial, try this: [https://nodesource.com/blog/an-absolute-beginners-guide-to-using-npm/](https://nodesource.com/blog/an-absolute-beginners-guide-to-using-npm/)

also, react-scripts TODO, tracked in #49

### React

React is a popular JS framework. It's great! Turning html components into variables that are manipulatable in code is great.

#### Technical Detail

If you don't have any React knowledge at all, then you should familiarize yourself with the basics. There are plenty of tutorials to get you up to speed. I enjoy React's official tutorial, here: https://reactjs.org/tutorial/tutorial.html. **In particular, make sure you read up to (and including) the Overview section**.

From the tutorial, you'll want to at least familiarize yourself with:

- what components are, and what the render method is

- what props are and what state is, and when components re-render

There's a couple other parts of React that we use heavily, that are not directly in the turorial. _These aren't strictly needed to start, but do come back to them if they come up._

You may want to know how conditional rendering works -- depending on what you do, it might come up. Here's a good explanation: https://reactjs.org/docs/conditional-rendering.html

Note that as you navigate our frontend, the URL in your web browser changes. A naive website implementation would have different html files for each page. But we only have one HTML file...what gives?
This is thanks to Routes and Switches, from `react-router`. You might want to know how they work, since they might come up too. This will help you to figure out what component is being rendered, based on a URL. For explanation, you can _skim_ https://v5.reactrouter.com/web/api/Route and https://v5.reactrouter.com/web/api/Switch. If there are important details, make sure to check the docs.

### JQuery

#### Technical Detail

You actually probably don't need to know how JQuery works, other than how its API is exposed as a dollar sign object. TODO good links? tracked in #49

### APIs and the Web

### HTTP Requests

What is? TODO Link to a small explanation. tracked in #49
Note that this is a thing for backend and frontend!

#### Technical Detail

TODO link to a small explanation. tracked in #49

### Async, Promises, and Callbacks

TODO one-sentence description if at all. tracked in #49

#### Technical Detail

TODO link to a small explanation. tracked in #49

Any linked explanation or explnation we write ought to discuss

- at a high level, what async programming is
- promises in vanilla JS first,
- and then how JQuery's AJAX works

## Battlecode-specific frontend knowledge

Here are (some) specifics about how Battlecode's frontend codebase is specifically set up and how it specifically works.

### Injection from the root up

So first, from the bottom, what creates our pages? Ultimately, our page is `public/index.html` with some js running.

#### Technical Detail

We serve, _at first_, a static webpage. Go to `public/index.html` to see it. It contains simply a div called "root", and also a lot of imports. Many of those imports are third-party imports, of CSS/JS that we pull from external websites, or that we have downloaded but made some small tweaks to. See the `public` folder.

But note also `src/index.js`, and especially its last few lines, is run on `public/index.html`. Look up how injecting a react root works (and add a link, or Nathan can dig it up too). I forget the end result, but basically, the js at `src/index.js` is shoved into that div called "root".

### Routes

#### Technical Detail

See `src/index.js` for how we expose a single-page app, with routes and matching components, and especially to see how we only expose some routes.

### Our API

TODO. tracked in #49

(hits backend, and sometimes hits other external sites too)

#### Technical Detail

TODO. tracked in #49

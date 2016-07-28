# My Cookbook
[![Dev Build Status](https://travis-ci.org/PeterMitrano/my_cookbook.svg?branch=alexa-sdk-src)](https://travis-ci.org/PeterMitrano/my_cookbook)
[![Master Build Status](https://travis-ci.org/PeterMitrano/my_cookbook.svg?branch=master)](https://travis-ci.org/PeterMitrano/my_cookbook)

#### An Alexa Skill to help out in the kitchen

## Development

Use `npm install` to get everything you need.
Run `grunt`. This will run jshint and generate jsdocs.

## Status & Thoughts

Let the interaction/conversation between the user and my_cookbook be modeled as a graph, with directed edges. The system starts by making one introductory query, and then the user responds. The response either falls as one of the valid edges from the current node of the graph, or it does not. If it does, then the system transitions to the node at the end of that edge. If it does not, then the system reports an error of sorts, telling the user it doesn't understand. So we need to have nodes, and they need to have incoming and outcoming edges. They need to have a statement of what we say. Each edge corresponds to an Intent. In order to track out session, we need to store our location in sessionAttributes. So, each node should be hashable and we can use a hash table to store the nodes in the graph.

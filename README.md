# Spawning and interacting with game elements
* spawn NPCs
    * NPC movement
    * set destination(s)
    * automatic cycling of detinations once reached
    * trail of last positions
* collision of "protagonist" with NPCs
    * camera shake effect to emphesis event
    * adjustment to length of "protagonists" trail after collision

# TODO -- fuck yeah
* [x] spawn 10 npc
* [x] set npc movement to go back and forth between 2 destinations
    * [x] allow movement
    * [x] setable destination
    * [x] setable secondary destination
    * [x] toggle 1st, 2nd destinations
    * [x] debug destinations as objects tend to get stuck at the start or at a destination
* [x] allow npc to cycle through a list of destinations
* [x] add trail of previous locations
* [x] consider collisions
    * [x] despawn an object
    * [x] add screen shake on impact with protagonist
* [ ] visual effects class
    * [ ] consider the possibility of subclassing entity to make a effemeral object for visual effects
* [ ] collision refinement
    * [ ] don't consider collision if the colliding objects are not on the same parallax value.
* [ ] allow bullet time for a "hero" entity
* [ ] allow bullet time to affect a list of entities
* [ ] allow scallable magnitude for the bullet effect

# TODO -- mehh, when I feel like it. maybe
* [ ] refactor code  # its getting messy
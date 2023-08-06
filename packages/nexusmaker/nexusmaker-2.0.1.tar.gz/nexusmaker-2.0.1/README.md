# NexusMaker

## Simply Generate Nexus Files

```
from nexusmaker import NexusMaker, Record


data = [
    Record(Language="A", Word="eye", Item="", Cognate="1"),
    Record(Language="A", Word="leg", Item="", Cognate="1"),
    Record(Language="A", Word="arm", Item="", Cognate="1"),
    
    Record(Language="B", Word="eye", Item="", Cognate="1"),
    Record(Language="B", Word="leg", Item="", Cognate="2"),
    Record(Language="B", Word="arm", Item="", Cognate="2"),
    
    Record(Language="C", Word="eye", Item="", Cognate="1"),
    # No ReCord for C 'leg'
    Record(Language="C", Word="arm", Item="", Cognate="3"),

    Record(Language="D", Word="eye", Item="", Cognate="1", loan=True),
    Record(Language="D", Word="leg", Item="", Cognate="1"),
    Record(Language="D", Word="leg", Item="", Cognate="2"),
    Record(Language="D", Word="arm", Item="", Cognate="2,3"),
]

maker = NexusMaker(data)

maker = NexusMakerAscertained(data)  # adds Ascertainment bias character

maker = NexusMakerAscertainedWords(data)  # adds Ascertainment character per word
nex = maker.make()
maker.write(nex, filename="output.nex")


```

### Version History:

* 2.0.1: minor bugfixes.
* 2.0: major refactor of testing and other components.
* 1.5: do more validation of cognate sets to detect possibly broken combined cognate sets.
* 1.4: normalise order of cognates (i.e. so 1,54 == 54,1).
* 1.3: handle cognates of form '1a'.
* 1.2: initial release.

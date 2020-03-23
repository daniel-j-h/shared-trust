# Shared Trust

Share secrets amongst a group of people whom you trust (or don't), where a subset can re-construct the secret.


## Overview

To start with an example
- you want to share your company's secret amongst the n=4 founders
- only if the t=3 (or more) founders agree, they are able to re-construct the secret

Another example
- you want to share your social media logins with your n=10 family members
- each family member will not be able to re-construct your social media logins
- only if t=7 family members agree that something happened to you they can re-construct your social media logins

The idea is to be able to represent and share this kind of trust digitally.


## Usage

Use the encode command to generate keys and shares

    ./bin/st encode -n 4 -t 3 "Secret to share with 4 people, any 3 of them can re-construct it"

which generates
- `key.*` these are the keys you hand out to the n=4 people, one key per individual
- `share.*` these are encrypted and signed shares to re-construct the secret using any t=3 keys

Use the decode command to re-construct the secret from keys and shares

    ./bin/st decode 0 1 3
    Secret to share with 4 people, any 3 of them can re-construct it

This re-constructs the secret based on
- keys `key.0`, `key.1`, and `key.3` from persons 0, 1, and 3
- share `share.0.1.3` which is the encrpted and signed secret matching the keys


Note:
- you can weight trust by handing out multiple keys per person
- hierarchical trust is possible by repeatedly encoding shares


## Real Talk

This is a cute prototype but I don't recommend using it for anything serious.
We simply generate n keys and generate all encrypted and signed permutations for these n keys; this will not scale (without tricks like hierarchical shares) for larger settings.


## More

- https://en.wikipedia.org/wiki/Secret_sharing
- https://en.wikipedia.org/wiki/Erasure_code
- https://en.wikipedia.org/wiki/Permutation
- https://en.wikipedia.org/wiki/Salsa20
- https://en.wikipedia.org/wiki/Poly1305


## License

Copyright © 2020 Daniel J. Hofmann

Distributed under the MIT License (MIT).

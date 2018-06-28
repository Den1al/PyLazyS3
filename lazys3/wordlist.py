# author:   @Daniel_Abeles
# date:     26/06/18 

class WordlistGenerator(object):

    common_envs = ('dev', 'development', 'stage',
                   's3', 'staging', 'prod', 'production', 'test')

    def __init__(self, wordlist_path: str, target: str):
        self.wordlist_path = wordlist_path
        self.target = target

    def _create_file_gen(self):
        with open(self.wordlist_path, 'r') as f:
            for line in f:
                yield line.strip()

    def _permute_envs(self, prefix: str):
        for env in self.common_envs:
            for fmt in ['%s-%s-%s', '%s-%s.%s', '%s-%s%s', '%s.%s-%s', '%s.%s.%s']:
                yield fmt % (self.target, prefix, env)

    def _permute_host(self, prefix: str):
        for fmt in ['%s.%s', '%s-%s', '%s%s']:
            yield fmt % (self.target, prefix)
            yield fmt % (prefix, self.target)

    def _create_gen(self):
        yield self.target

        for prefix in self._create_file_gen():
            yield from self._permute_envs(prefix)
            yield from self._permute_host(prefix)

    def __iter__(self):
        return self._create_gen()
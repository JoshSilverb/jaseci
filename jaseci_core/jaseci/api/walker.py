"""
Walker api functions as a mixin
"""
from jaseci.actor.walker import walker
from jaseci.graph.node import node
from jaseci.actor.sentinel import sentinel
from jaseci.utils.utils import b64decode_str


class walker_api():
    """
    Walker APIs
    """

    def api_walker_create(self, snt: sentinel = None,
                          code: str = '', encoded: bool = False):
        """
        Create blank or code loaded walker and return object
        """
        if (encoded):
            code = b64decode_str(code)
        walk = snt.register_walker(code)
        if(walk):
            return walk.serialize()
        else:
            return [f'Walker not created, invalid code!']

    def api_walker_list(self, snt: sentinel = None, detailed: bool = False):
        """
        List walkers known to sentinel
        """
        walks = []
        for i in snt.walker_ids.obj_list():
            walks.append(i.serialize(detailed=detailed))
        return walks

    def api_walker_delete(self, wlk: walker, snt: sentinel = None):
        """
        Permanently delete walker with given id
        """
        wlkid = wlk.id
        snt.walker_ids.destroy_obj(wlk)
        return [f'Walker {wlkid} successfully deleted']

    def api_walker_code_get(self, wlk: walker, snt: sentinel = None):
        """
        Get sentinel implementation in form of Jac source code
        """
        return wlk._jac_ast.get_text()

    def api_walker_code_set(self, code: str, snt: sentinel = None,
                            encoded: bool = False):
        """
        Set sentinel implementation with Jac source code
        """

    def api_walker_spawn(self, name: str, snt: sentinel = None):
        """
        Creates new instance of walker and returns new walker object
        """
        wlk = snt.spawn(name)
        if(wlk):
            return wlk.serialize()
        else:
            return [f'Walker not found!']

    def api_walker_unspawn(self, wlk: walker):
        """
        Delete instance of walker (not implemented yet)
        """

        return []

    def api_walker_prime(self, wlk: walker, nd: node = None, ctx: dict = {}):
        """
        Assigns walker to a graph node and primes walker for execution
        """
        wlk.prime(nd, prime_ctx=ctx)
        return [f'Walker primed on node {nd.id}']

    def api_walker_run(self, wlk: walker):
        """
        Executes walker (assumes walker is primed)
        """
        wlk.run()
        return wlk.report

    def api_walker_primerun(self, name: str, nd: node = None, ctx: dict = {},
                            snt: sentinel = None):
        """
        Creates walker instance, primes walker on node, executes walker,
        reports results, and cleans up walker instance.
        """
        wlk = snt.spawn(name)
        if(not wlk):
            return [f'Walker {name} not found!']
        wlk.prime(nd, prime_ctx=ctx)
        res = self.api_walker_run(wlk)
        wlk.destroy()
        return res

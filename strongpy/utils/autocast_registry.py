class CastRegistry:
    __casters = {}

    @staticmethod
    def register_cast(from_type, to_type, caster):
        if CastRegistry.__casters.get(from_type, None) is None:
            CastRegistry.__casters[from_type] = dict()

        if CastRegistry.__casters[from_type].get(to_type, None) is not None:
            print("Cast already registered.")
            raise NotImplementedError()
        else:
            CastRegistry.__casters[from_type][to_type] = caster

    @staticmethod
    def deregister_cast(from_type, to_type):
        if CastRegistry.__casters.get(from_type, None) is not None:
            if CastRegistry.__casters[from_type].get(to_type, None) is not None:
                del CastRegistry.__casters[from_type][to_type]
            else:
                print("Cast does not exist")
                raise NotImplementedError()
        else:
            print("No casts are registrereaded for this type")
            raise NotImplementedError()

    @staticmethod
    def cast(value, target_type):
        if CastRegistry.__casters.get(type(value), None) is None:
            print("no casters defined for this type")
            raise NotImplementedError
        elif CastRegistry.__casters[type(value)].get(target_type, None) is None:
            print("no casters defined for this conversion")
            raise NotImplementedError
        else:
            caster = CastRegistry.__casters[type(value)][target_type]
            try:
                result = caster(value)
            except Exception as e:
                print("While casting this type an exception occured")
                raise NotImplementedError

            if type(result) != target_type:
                print("The registered converter has not produced a value of type X")
                raise NotImplementedError
            
            return result


CastRegistry.register_cast(int, str, lambda i: str(i))
CastRegistry.register_cast(bool, str, lambda b: str(b))

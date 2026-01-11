class UnsetType:
    def __repr__(self) -> str:
        return 'UNSET'

    def __bool__(self) -> bool:
        return False


type Unset = UnsetType
UNSET: Unset = UnsetType()

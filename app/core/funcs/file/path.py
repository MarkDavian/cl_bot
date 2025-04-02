from dataclasses import dataclass


@dataclass(frozen=True)
class Certificates:
    path = 'storage/certificates/'


@dataclass(frozen=True)
class Tmp:
    path = 'storage/tmp/'
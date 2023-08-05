import os
from hypothesis import settings, Verbosity, HealthCheck

settings.register_profile("ci", max_examples=100)
settings.register_profile("dev", max_examples=50)
settings.register_profile("debug", max_examples=10, verbosity=Verbosity.verbose)

settings.register_profile(
    "coverage",
    max_examples=50,
    suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow),
)

settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "dev"))

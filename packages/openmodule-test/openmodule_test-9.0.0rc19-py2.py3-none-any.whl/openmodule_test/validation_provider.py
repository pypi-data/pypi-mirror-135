from openmodule.core import core
from openmodule.utils.validation import ValidationProvider
from openmodule_test.core import OpenModuleCoreTestMixin


class TestValidationProvider(ValidationProvider):
    __test__ = False  # otherwise pytest thinks this is a testcase


class ValidationProviderTestMixin(OpenModuleCoreTestMixin):
    """
    ValidationProviderTestMixin with helper functions for testing validation providers
    * set the validation_provider_class
    """
    validation_provider_class = None

    @classmethod
    def setUpClass(cls) -> None:
        assert cls.validation_provider_class, "set a validation_provider_class"
        return super().setUpClass()

    def setUp(self):
        super().setUp()
        self.validation_provider = self.validation_provider_class(core())

    def tearDown(self):
        self.validation_provider.shutdown()
        super().tearDown()

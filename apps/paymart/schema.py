import graphene
import binascii
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType, ObjectType
from graphql.error import GraphQLError
from apps.user_profile.models import User
from typing import TYPE_CHECKING, Type, Union
# from saleor.graphql.core.utils import from_global_id_or_error
from .models import Contract


def from_global_id_or_error(
    id: str, only_type: Union[ObjectType, str] = None, raise_error: bool = False
):
    """Resolve database ID from global ID or raise ValidationError.

    Optionally validate the object type, if `only_type` is provided,
    raise GraphQLError when `raise_error` is set to True.
    """
    try:
        _type, _id = graphene.Node.from_global_id(id)
    except (binascii.Error, UnicodeDecodeError, ValueError):
        raise GraphQLError(f"Couldn't resolve id: {id}.")

    if only_type and str(_type) != str(only_type):
        if not raise_error:
            return _type, None
        raise GraphQLError(f"Must receive a {only_type} id.")
    return _type, _id


class ContractType(DjangoObjectType):
    class Meta:
        model = Contract
        filter_fields = ['user']
        interfaces = (relay.Node,)


class ContractQuery(ObjectType):
    contract = relay.Node.Field(ContractType)
    contracts = DjangoFilterConnectionField(ContractType)

    def resolve_contract(self, info, **kwargs):
        id = kwargs.get('id')
        _, id = from_global_id_or_error(id, ContractType)

        if id is not None:
            return Contract.objects.get(pk=id)

        return None

    def resolve_contracts(self, info, **kwargs):
        user_id = kwargs.get('user')

        if user_id is not None:
            _, user_id = from_global_id_or_error(user_id, User)
            return Contract.objects.filter(user_id=user_id)
        return Contract.objects.all()


class ContractInput(graphene.InputObjectType):
    user_id = graphene.Int()
    product_variant_id = graphene.Int()
    status = graphene.String()
    products = graphene.String()
    limit = graphene.String()
    payment_date = graphene.String()
    buyer_phone = graphene.String()


class CreateContract(graphene.Mutation):
    contract = graphene.Field(ContractType)

    class Arguments:
        input = ContractInput(required=True)

    def mutate(self, info, input):
        _, user_id = from_global_id_or_error(input.user_id, User)
        _, product_variant_id = from_global_id_or_error(input.product_variant_id)
        contract = Contract(
            user_id=user_id,
            product_variant_id=product_variant_id,
            status=input.status,
            products=input.products,
            limit=input.limit,
            payment_date=input.payment_date,
            buyer_phone=input.buyer_phone,
        )
        contract.save()
        return CreateContract(contract=contract)


class UpdateContract(graphene.Mutation):
    contract = graphene.Field(ContractType)

    class Arguments:
        id = graphene.String(required=True)
        input = ContractInput(required=True)

    def mutate(self, info, id, input):
        _, contract_id = from_global_id_or_error(id, ContractType)
        contract = Contract.objects.filter(pk=contract_id).first()

        if input.user_id:
            _, user_id = from_global_id_or_error(input.user_id, User)
            contract.user_id = user_id

        if input.product_variant_id:
            _, product_variant_id = from_global_id_or_error(input.product_variant_id)
            contract.product_variant_id = product_variant_id
        #
        if input.status:
            contract.status = input.status

        if input.products:
            contract.products = input.products
        if input.limit:
            contract.limit = input.limit

        if input.payment_date:
            contract.payment_date = input.payment_date

        if input.buyer_phone:
            contract.buyer_phone = input.buyer_phone

        contract.save()
        return UpdateContract(contract=contract)


class DeleteContract(graphene.Mutation):
    contract = graphene.Field(ContractType)

    class Arguments:
        id = graphene.String(required=True)

    def mutate(self, info, id):
        _, contract_id = from_global_id_or_error(id, ContractType)
        contract = Contract.objects.filter(pk=id).first()
        contract.delete()
        return DeleteContract(contract=contract)


class ContractMutations(graphene.ObjectType):
    create_contract = CreateContract.Field()
    update_contract = UpdateContract.Field()
    delete_contract = DeleteContract.Field()

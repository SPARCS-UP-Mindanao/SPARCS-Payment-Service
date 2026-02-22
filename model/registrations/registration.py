from enum import Enum
from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    HttpUrl,
    root_validator,
    validator,
)


class SocialMedia(BaseModel):
    linkedIn: Optional[HttpUrl] = Field(None, title='LinkedIn Profile URL')
    facebook: Optional[HttpUrl] = Field(None, title='Facebook Profile URL')


class TicketTypes(str, Enum):
    CODER = 'coder'
    KASOSYO = 'kasosyo'


class TShirtType(str, Enum):
    UNISEX = 'unisex'
    FEMALE = 'female'


class TShirtSize(str, Enum):
    XS = 'XS'
    S = 'S'
    M = 'M'
    L = 'L'
    XL = 'XL'
    XXL = 'XXL'
    XXXL = 'XXXL'


class Registration(BaseModel):
    firstName: str = Field(..., title='First Name')
    lastName: str = Field(..., title='Last Name')
    nickname: str = Field(..., title='Nickname')
    pronouns: str = Field(..., title='Pronouns')
    email: EmailStr = Field(..., title='Email')
    eventId: str = Field(..., title='Pycon Event Id')
    contactNumber: str = Field(..., title='Contact Number')
    organization: str = Field(..., title='Affiliated Company or Organization')
    jobTitle: str = Field(..., title='Job Title', description='Your current job title or role in tech')
    facebookLink: HttpUrl = Field(..., title='Facebook Profile URL')
    linkedInLink: Optional[HttpUrl] = Field(None, title='LinkedIn Profile URL')

    ticketType: TicketTypes = Field(title='Ticket Type', description='Type of ticket you are registering for')
    sprintDay: bool = Field(
        ..., title='Sprint Day Participation', description='Will you be participating in the sprint day?'
    )

    availTShirt: bool = Field(
        ..., title='T-Shirt Availability', description='Do you want to buy an exclusive PyCon T-shirt?'
    )
    shirtType: Optional[TShirtType] = Field(
        None, title='T-Shirt Type', description='Type of the T-shirt you want to order'
    )
    shirtSize: Optional[TShirtSize] = Field(
        None, title='T-Shirt Size', description='Size of the T-shirt you want to order'
    )

    communityInvolvement: bool = Field(
        ..., title='Community Involvement', description='Are you a member of any local tech community?'
    )
    futureVolunteer: bool = Field(
        ..., title='Future Volunteer Interest', description='Would you like to volunteer in the future?'
    )
    dietaryRestrictions: Optional[str] = Field(
        None, title='Dietary Restrictions', description='Any dietary restrictions or allergies'
    )
    accessibilityNeeds: Optional[str] = Field(
        None, title='Accessibility Needs', description='Any specific accessibility needs or requests'
    )

    discountCode: Optional[str] = Field(
        None, title='Discount Code', description='If you have a discount code, please enter it here'
    )
    validIdObjectKey: str = Field(..., title='Image ID Object Key')

    @validator('firstName', 'lastName', 'nickname')
    def normalize_names(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Name fields cannot be empty')

        return ' '.join(word.capitalize() for word in v.split())

    @root_validator
    def check_shirt_availability(cls, values):
        avail_tshirt = values.get('availTShirt')
        shirt_type = values.get('shirtType')
        shirt_size = values.get('shirtSize')

        if avail_tshirt and (shirt_type is None or shirt_size is None):
            raise ValueError('If availTShirt is True, then shirtType and shirtSize must be provided.')

        return values

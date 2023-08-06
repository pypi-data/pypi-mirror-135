"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
"""
from cfn_policy_validator.parsers.output import Policy, Resource


class S3BucketPolicyParser:
    """ AWS::S3::BucketPolicy
    """

    def __init__(self):
        self.bucket_policies = []

    def parse(self, _, resource):
        evaluated_resource = resource.eval(bucket_policy_schema)
        properties = evaluated_resource['Properties']

        bucket_name = properties['Bucket']
        policy_document = properties['PolicyDocument']

        policy = Policy('BucketPolicy', policy_document)
        resource = Resource(bucket_name, 'AWS::S3::Bucket', policy)

        self.bucket_policies.append(resource)

    def get_policies(self):
        return self.bucket_policies


bucket_policy_schema = {
    'type': 'object',
    'properties': {
        'Properties': {
            'type': 'object',
            'properties': {
                'Bucket': {
                    'type': 'string'
                },
                'PolicyDocument': {
                    'type': 'object'
                }
            },
            'required': ['Bucket', 'PolicyDocument']
        }
    },
    'required': ['Properties']
}


class S3AccessPointPolicyParser:
    """ AWS::S3::AccessPoint
    """

    def __init__(self):
        self.access_point_policies = []

    def parse(self, resource_name, resource):
        evaluated_resource = resource.eval(access_point_policy_schema)
        properties = evaluated_resource['Properties']

        access_point_name = properties.get('Name', resource_name)
        policy_document = properties['Policy']

        policy = Policy('AccessPointPolicy', policy_document)
        resource = Resource(access_point_name, 'AWS::S3::AccessPoint', policy)

        self.access_point_policies.append(resource)

    def get_policies(self):
        return self.access_point_policies


access_point_policy_schema = {
    'type': 'object',
    'properties': {
        'Properties': {
            'type': 'object',
            'properties': {
                'Name': {
                    'type': 'string'
                },
                'Policy': {
                    'type': 'object'
                }
            },
            'required': ['Policy']
        }
    },
    'required': ['Properties']
}


class S3MultiRegionAccessPointPolicyParser:
    """ AWS::S3::MultiRegionAccessPointPolicy
    """

    def __init__(self):
        self.multi_region_access_point_policies = []

    def parse(self, _, resource):
        evaluated_resource = resource.eval(multi_region_access_point_policy_schema)
        properties = evaluated_resource['Properties']

        mrap_name = properties['MrapName']
        policy = properties['Policy']

        policy_document = Policy('MultiRegionAccessPointPolicy', policy)
        resource = Resource(mrap_name, 'AWS::S3::MultiRegionAccessPoint', policy_document)

        self.multi_region_access_point_policies.append(resource)

    def get_policies(self):
        return self.multi_region_access_point_policies


multi_region_access_point_policy_schema = {
    'type': 'object',
    'properties': {
        'Properties': {
            'type': 'object',
            'properties': {
                'MrapName': {
                    'type': 'string'
                },
                'Policy': {
                    'type': 'object'
                }
            },
            'required': ['MrapName', 'Policy']
        }
    },
    'required': ['Properties']
}

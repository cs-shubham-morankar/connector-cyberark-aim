## About the connector

CyberArk Application Identity Manager (AIM) is a key component in CyberArk's Privileged Access Security suite. It helps
manage and secure credentials used by applications and services by providing secure retrieval of passwords and other
sensitive data.
<p>This document provides information about the CyberArk AIM Connector, which facilitates automated interactions, with a CyberArk AIM server using FortiSOAR&trade; playbooks. Add the CyberArk AIM Connector as a step in FortiSOAR&trade; playbooks and perform automated operations with CyberArk AIM.</p>

### Version information

Connector Version: 1.1.0

Authored By: Fortinet

Certified: No

## Release Notes for version 1.1.0

Following enhancements have been made to the CyberArk AIM Connector in version 1.1.0:
<ul>
<li><p>The following new parameters have been added to the connector configuration:</p>

<ul>
<li><p>Objects</p></li>
<li><p>Folder</p></li>
<li><p>Security Level</p></li>
</ul></li>
<li><p>Removed the <code>Objects</code> parameter from the <code>Get Password</code> operation.</p>

</ul>

## Installing the connector

<p>Use the <strong>Content Hub</strong> to install the connector. For the detailed procedure to install a connector, click <a href="https://docs.fortinet.com/document/fortisoar/0.0.0/installing-a-connector/1/installing-a-connector" target="_top">here</a>.</p><p>You can also use the <code>yum</code> command user to install the connector:</p>

```
sudo yum install cyops-connector-cyberark-aim
```

## Prerequisites to configuring the connector

- You must have the credentials of CyberArk AIM server to which you will connect and perform automated operations.
- The FortiSOAR&trade; server should have outbound connectivity to port 443 on the CyberArk AIM server.

## Minimum Permissions Required

- Not applicable

## Configuring the connector

For the procedure to configure a connector,
click [here](https://docs.fortinet.com/document/fortisoar/0.0.0/configuring-a-connector/1/configuring-a-connector)

### Configuration parameters

<p>In FortiSOAR&trade;, on the Connectors page, click the <strong>CyberArk AIM</strong> connector row (if you are in the <strong>Grid</strong> view on the Connectors page) and in the <strong>Configurations</strong> tab enter the required configuration details:</p>
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Server URL</td><td>URL of the CyberArk server to which you will connect and perform automated operations.
</td>
</tr><tr><td>Application ID</td><td>Application ID that has been issued to you by CyberArk, which is used for the password retrieval process.See the "Creating an application in CyberArk" section for the procedure on how to create an application in CyberArk.
</td>
</tr><tr><td>Safe Name</td><td>Name of the Safe that stores the credentials, including passwords.
</td>
<tr><td>Objects<br></td><td>Specify the comma-separated object names of the Safe that stores the credentials, including passwords.<br>
<tr><td>Folder<br></td><td>Specify the name of the Folder that stores the credentials, including passwords. Default, it set as "root".<br>
<tr><td>Security Level<br></td><td>Specify the security level of the CyberArk.<br>
</tr><tr><td>Authentication Type</td><td>Specify the type of authentication of the CyberArk server to which you will connect and perform automated operations. By default, this option is set as "No Auth".
<br><strong>If you choose 'Basic Auth'</strong><ul><li>Username: Specify the username to access the CyberArk server to connect and perform automated operations.</li><li>Password: Specify the password to access the CyberArk server to connect and perform automated operations.</li></ul></td>
</tr><tr><td>Verify SSL</td><td>Specifies whether the SSL certificate for the server is to be verified or not. <br/>By default, this option is set to True.</td></tr>
</tbody></table>

## Actions supported by the connector

The following automated operations can be included in playbooks and you can also use the annotations to access
operations:
<table border=1><thead><tr><th>Function</th><th>Description</th><th>Annotation and Category</th></tr></thead><tbody><tr><td>Get Password</td><td>Enables applications to retrieve passwords from the Central Credential Provider.</td><td>get_password <br/>Investigation</td></tr>
</tbody></table>

### operation: Get Password

#### Input parameters

<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Folder</td><td>Specifies the name of the folder where the password is stored. Default, it set as "Root".
</td></tr><tr><td>Username</td><td>Defines search criteria according to the Username account property.
</td></tr><tr><td>Address</td><td>Defines search criteria according to the Address account property.
</td></tr><tr><td>Policy ID</td><td>Defines the format that will be used in the Set Policy ID method.
</td></tr><tr><td>Additional Properties</td><td>(Optional) Specify the additional properties, in the JSON format, that you want to retrieve the password from Central Credential Provider. The additional properties signify additional fields associated with the application.
</td></tr></tbody></table>

#### Output

The output contains the following populated JSON schema:

<pre>{
    "Content": "",
    "UserName": "",
    "Address": "",
    "Database": "",
    "PasswordChangeInProcess": ""
}</pre>

## Included playbooks

The `Sample - CyberArk AIM - 1.1.0` playbook collection comes bundled with the CyberArk AIM connector. These playbooks
contain steps using which you can perform all supported actions. You can see bundled playbooks in the **Automation** > *
*Playbooks** section in FortiSOAR&trade; after importing the CyberArk AIM connector.

- Get Password

----
**Note**:

If you are planning to use any of the sample playbooks in your environment, ensure that you clone those playbooks and
move them to a different collection since the sample playbook collection gets deleted during connector upgrade and
delete.

----

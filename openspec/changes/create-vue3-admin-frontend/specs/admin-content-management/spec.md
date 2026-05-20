## ADDED Requirements

### Requirement: Tag management interface
The system SHALL allow authorized administrators to list, create, update, and delete tags using the backend tag endpoints, including pagination state and API validation feedback.

#### Scenario: Administrator creates a tag successfully
- **WHEN** an authorized administrator submits a valid tag creation form
- **THEN** the application creates the tag through the backend API and updates the tag listing to include the new record

#### Scenario: Tag creation is rejected by the backend
- **WHEN** the backend returns a validation or conflict error for the submitted tag
- **THEN** the application preserves the form state and displays the error in a way the administrator can act on

### Requirement: Post listing and editorial actions
The system SHALL allow authorized administrators to list posts, filter by status, create new posts, update existing posts, and trigger publish or archive actions from the admin interface.

#### Scenario: Administrator filters posts by status
- **WHEN** an administrator selects a post status filter in the listing view
- **THEN** the application reloads the list using the backend status query parameter and displays the filtered result set

#### Scenario: Administrator publishes a ready post
- **WHEN** an administrator triggers the publish action for a post that satisfies backend rules
- **THEN** the application calls the publish endpoint and refreshes the post state shown in the interface

### Requirement: Editable post content retrieval
The system SHALL retrieve the editable HTML, summary, tags, and image metadata for an existing post before rendering the post edit experience, using either an expanded post detail contract or a dedicated editorial detail endpoint.

#### Scenario: Administrator opens an existing post for editing
- **WHEN** an administrator navigates to the post edit route
- **THEN** the application loads the post metadata together with its editable content payload before enabling form editing

### Requirement: Post image upload and lifecycle actions
The system SHALL allow authorized administrators to upload images for a post, display the uploaded image metadata in the editing workflow, and use a stable backend-provided image identifier for later download or removal actions.

#### Scenario: Administrator uploads a valid image
- **WHEN** an administrator uploads a JPEG, PNG, or WebP file to a post
- **THEN** the application sends the multipart request, receives the stored image metadata, and renders the uploaded image in the post editing workflow

#### Scenario: Administrator removes an uploaded image
- **WHEN** an administrator requests deletion of an image using its stable identifier
- **THEN** the application calls the backend delete action and removes the image from the editing workflow after a successful response
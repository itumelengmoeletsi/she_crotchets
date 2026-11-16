from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.projects import Project, ProjectStatus as ModelProjectStatus
from app.schemas.projects_schema import ProjectCreate, ProjectUpdate

def create_project(db: Session, project_data: ProjectCreate, user_id: int):
    # Exclude status from dump so we explicitly set it using sqlalchemy Enum
    project_dict = project_data.model_dump(exclude={"status"})

    # create project
    new_project = Project(
        **project_dict,
        user_id=user_id,
        status=ModelProjectStatus.OPEN
    )

    db.add(new_project)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details="Database error while creating project"
        )

    db.refresh(new_project)
    return new_project

def update_job(db: Session, project_id: int, project_data: ProjectUpdate, user_id: int):
    # Filter by both project ID and user_id to enforce ownership
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == user_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied."
        )

    update_data = project_data.dict(exclude_unset=True) # Only update what the user sent

    for key, value in update_data.items():
        if key == "status" and value is not None:
            # Convert Pydantinc status value ("open"/ "closed") to SQLAlchemy
            value == ModelProjectStatus(value.value if hasattr(value, "value") else value.lower())
        setattr(project, key, value)

    # save to db
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while updating project."
        )

    db.refresh(project)
    return project
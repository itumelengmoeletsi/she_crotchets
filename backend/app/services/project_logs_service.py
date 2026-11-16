from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.project_logs import ProjectLog
from app.models.projects import Project
from app.schemas.project_logs_schema import ProjectLogsCreate, ProjectLogsUpdate

def create_project_log(db: Session, log_data: ProjectLogsCreate, project_id: int, user_id: int):
    # 1. Verify the parent project exists and belongs to the user
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == user_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied."
        )

    # 2. Unpack validated schema fields and attach project_id
    new_log = ProjectLog(
        **log_data.model_dump(),
        project_id=project_id
    )

    db.add(new_log)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while creating project log"
        )

    db.refresh(new_log)
    return new_log

def update_project_log(db: Session, log_id: int, log_data: ProjectLogsUpdate, user_id: int):
    # Join with Project to ensure the log belongs to a project owned by user_id
    log = (
        db.query(ProjectLog)
        .join(Project, ProjectLog.project_id == Project.id)
        .filter(
            ProjectLog.id == log_id,
            Project.user_id == user_id
        ).first()
    )

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project log not found or access denied."
        )

    update_data = log_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(log, key, value)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while updateing project log."
        )

    db.refresh(log)
    return log
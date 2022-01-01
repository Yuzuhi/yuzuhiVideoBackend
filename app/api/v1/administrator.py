

router = APIRouter()



@router.post('/add/administrator/', name="添加管理员")
async def admin_create(
        admin_info: AdministratorCreate,
        db: Session = Depends(utils.get_db),
):
    obj_info = curd_admin.create(db, obj_in=admin_info)
    return response_code.response_200(data=obj_info)

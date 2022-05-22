# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import Column, Integer, String, ForeignKey, delete, select
#
# from src.database.database_metadata import Base
#
#
# class Barcode(Base):
#     __tablename__ = 'barcode'
#
#     barcode = Column(String, primary_key=True, index=True)
#     alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'))
#
#
# class BarcodeDatabaseHandler:
#     @staticmethod
#     async def get_barcodes(db: AsyncSession, barcodes: list[str]) -> list[Barcode]:
#         query = select(Barcode).where(Barcode.barcode.in_(barcodes))
#         db_barcodes = await db.execute(query)
#         return db_barcodes.scalars().all()
#
#     @staticmethod
#     async def delete_barcode(db: AsyncSession, barcode: str) -> None:
#         query = delete(Barcode).\
#             where(Barcode.barcode == barcode)
#         await db.execute(query)

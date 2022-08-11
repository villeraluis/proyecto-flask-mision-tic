from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.reservation import Reservation
from models.room import Room
from models.user import User

from utils.db import db
from forms.reservationForm import ReservationForm

reservas = Blueprint("reservas", __name__)

@reservas.route('/admin')
def index_admin():
    reservations = Reservation.query.all()  
    return render_template('reservas/indexAdmin.html',reservations=reservations)

@reservas.route("admin/crear/<idh>", methods=['GET'])      
@reservas.route('admin/crear', methods=['GET','POST'])
def create_admin(idh=None):
    form = ReservationForm()
       
    form.room_id.choices = [(room.id, room.number) for room in Room.query.all()]
    form.user_id.choices = [(client.id_number, client.name) for client in User.query.all()]
    if(idh is not None):
        form.room_id.default=idh
        form.process()
    
    if form.validate_on_submit():
        date_from=form.date_from.data
        date_to=form.date_to.data
        status='Realizada - Activa'
        room_id=form.room_id.data
        user_id=form.user_id.data
        
        reservation = Reservation()
        reservation.date_from=date_from
        reservation.date_to=date_to
        reservation.status=status
        reservation.room_id=room_id
        reservation.user_id=user_id

        db.session.add(reservation)
        db.session.commit()

        flash('Reserva Creada Correctamente!')

        return redirect(url_for('reservas.index_admin'))
    
    return render_template('reservas/createAdmin.html',form=form)


@reservas.route('/ver_reservas_admin/<id>',methods=['GET'])
def show_admin(id):
    reservation = Reservation.query.get(id)  
    diffDate = reservation.date_to - reservation.date_from             
    return render_template('reservas/showAdmin.html',reservation=reservation,diffDate=diffDate)

@reservas.route("admin/actualizar/<id>", methods=["GET", "POST"])
def update_admin(id):
    reservation = Reservation.query.get(id)
    form = ReservationForm(obj=reservation)

    form.room_id.choices = [(room.id, room.number) for room in Room.query.all()]
    form.user_id.choices = [(client.id_number, client.name) for client in User.query.all()]
    form.room_id.default=reservation.room_id
    form.user_id.default=reservation.user_id
    form.process()
    
    if form.validate_on_submit():
        date_from=form.date_from.data
        date_to=form.date_to.data
        status='Editada - Activa'
        room_id=form.room_id.data
        user_id=form.user_id.data
        
        reservation.date_from=date_from
        reservation.date_to=date_to
        reservation.status=status
        reservation.room_id=room_id
        reservation.user_id=user_id

        db.session.commit()

        flash('Reserva Actialuizada Correctamente!')

        return redirect(url_for('reservas.index_admin'))
                        
    return render_template('reservas/update_admin.html',form=form, id=id)



@reservas.route("/borrar_admin/<id>", methods=["GET"])
def delete_admin(id):
    reservation = Reservation.query.get(id) 
     
    db.session.delete(reservation)
    db.session.commit()
    flash('Reserva Borrada Correctamente!')
    
    return redirect(url_for('reservas.index_admin'))



@reservas.route('/user')
def index_user():  
    labelCurrent='Mis Reservas'
    return render_template('reservas/indexUser.html',labelCurrent=labelCurrent)






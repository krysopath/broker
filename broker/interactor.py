#!/usr/bin/env python3
# coding=utf-8
from tbx_dbio import DataSet, DataModel
from fractions import Fraction as Fraction
__dbfile__ = '%s-fuels.db'


class FuelModel(DataModel):
    schema = (
        ('_C', ""),
        ('_H', ""),
        ('_N', ""),
        ('_S', ""),
        ('_O', ""),
        ('_Cl', ""),
        ('_H2O', ""),
        ('_Ash', ""),
        ('_F', ""),
        ('_C', ""),
    )
    names = [name[0] for name in schema]

    def __init__(self, tablename, schema, dbpath):
        super(FuelModel, self).__init__(tablename, schema, dbpath)


class Fuel(DataSet):
    __elementarfaktor = {
        'Boje': {
            '_C': 348,
            '_H': 938,
            '_S': 104.6,
            '_O': -108,
            '_H2O': -24.5,
        },
        'Dulong': {
            '_C': 339,
            '_H': 1214.17,
            '_N': 62.8,
            '_O': -151.77,
            '_H20': -24.5,
        },
        'Michel': {
            '_C': 340.4,
            '_H': 1017.4,
            '_N': 62.8,
            '_O': -98.4,
            '_H20': -24.45,
        },
        'Verbandsformel': {
            '_C': 339.13,
            '_H': 1214.17,
            '_S': 104.67,
            '_O': -151.77,
            '_H20': -24.42,
        }
    }
    __andere = {
        'Luftbedarf': {
            '_C': 1.867,
            '_H': 5.6,
            '_S': 0.7,
            '_O': -0.7,
        },
        'Rauchgas': {
            '_C': 8.889,
            '_H': 32.267,
            '_S': 3.3333,
            '_O': -2.633,
            '_H2O': 1.244,
            '_N': 0.8,
        }
    }
    schema = {_name: type(_type)
              for _name, _type
              in FuelModel.schema}

    def __init__(self, fuelname='', *initial_data, **kwargs):
        super(Fuel, self).__init__(*initial_data, **kwargs)
        #self.name = fuelname

    def __str__(self):
        data = {k.split('_')[1]: v for k, v in self if v is not None}
        return data.__str__()

    def __setitem__(self, item, val):
        if item in self.__data__:
            return setattr(self, item, val)

    @property
    def F(self):
        return str(self._F)

    @property
    def O(self):
        return str(self._O)

    @property
    def N(self):
        return str(self._N)

    @property
    def S(self):
        return str(self._S)

    @property
    def Cl(self):
        return str(self._Cl)

    @property
    def H(self):
        return str(self._H)

    @property
    def Ash(self):
        return str(self._Ash)

    @property
    def H2O(self):
        return str(self._H2O)

    @property
    def C(self):
        return str(self._C)

    @C.setter
    def C(self, x):
        x = Fraction(x)
        if 0 <= x <= 100:
            self.remove('_C')
            self.mixin('_C', x)
            self._C = x
        else:
            raise ValueError('number needs to be between 0 and 100 %mas')

    @F.setter
    def F(self, x):
        x = Fraction(x)
        if 0 <= x <= 100:
            self.remove('_F')
            self.mixin('_F', x)
            self._F = x
        else:
            raise ValueError('number needs to be between 0 and 100 %mas')

    @O.setter
    def O(self, x):
        x = Fraction(x)
        if 0 <= x <= 100:
            self.remove('_O')
            self.mixin('_O', x)
            self._O = x
        else:
            raise ValueError('number needs to be between 0 and 100 %mas')

    @H.setter
    def H(self, x):
        x = Fraction(x)
        if 0 <= x <= 100:
            self.remove('_H')
            self.mixin('_H', x)
            self._H = x
        else:
            raise ValueError('number needs to be between 0 and 100 %mas')

    @N.setter
    def N(self, x):
        x = Fraction(x)
        if 0 <= x <= 100:
            self.remove('_N')
            self.mixin('_N', x)
            self._N = x
        else:
            raise ValueError('number needs to be between 0 and 100 %mas')

    @S.setter
    def S(self, x):
        x = Fraction(x)
        if 0 <= x <= 100:
            self.remove('_S')
            self.mixin('_S', x)
            self._S = x
        else:
            raise ValueError('number needs to be between 0 and 100 %mas')

    @Cl.setter
    def Cl(self, x):
        x = Fraction(x)
        if 0 <= x <= 100:
            self.remove('_Cl')
            self.mixin('_Cl', x)
            self._Cl = x
        else:
            raise ValueError('number needs to be between 0 and 100 %mas')

    @Ash.setter
    def Ash(self, x):
        x = Fraction(x)
        if 0 <= x <= 100:
            self.remove('_Ash')
            self.mixin('_Ash', x)
            self._Ash = x
        else:
            raise ValueError('number needs to be between 0 and 100 %mas')

    @H2O.setter
    def H2O(self, x):
        if 0 <= x <= 100:
            x = Fraction(x)
            self.remove('_H2O')
            self.mixin('_H2O', x)
            self._H2O = x
        else:
            raise ValueError('number needs to be between 0 and 100 %mas')

    def mixin(self, element, amount):
        for old_element, old_value in self:
            if old_value:
                if old_element != element:
                    setattr(self, old_element, Fraction(old_value * (1 - amount)))
                else:
                    setattr(self, old_element, Fraction(amount))

    def remove(self, element):
        if self[element]:
            for old_element, old_value in self:
                if old_value:
                    if old_element != element:
                        try:
                            setattr(self, old_element, Fraction(
                                Fraction(old_value) * Fraction(1 / (1 - Fraction(self[element])))
                            ))
                        except ZeroDivisionError:
                            setattr(self, old_element, Fraction(0))
                            self[old_element] = Fraction(0)
                    else:
                        pass

    def _heizwert(self, formel='Boje'):
        hzwert = 0
        for element, anteil in self:
            try:
                if anteil > 0:
                    add = anteil * self.__elementarfaktor[formel][element] * 100
                    hzwert += add
            except KeyError as ke:
                print(ke)
            except TypeError as te:
                print(te)
            except Exception as e:
                raise e

        return hzwert

    def dulong(self):
        return self._heizwert('Dulong')

    def boje(self):
        return self._heizwert('Boje')

    def michel(self):
        return self._heizwert('Michel')

    def verbandsformel(self):
        return self._heizwert('Verbandsformel')


class Interactor:
    def __init__(self, for_user, datamodel, dataset):
        self.user = for_user
        self.dataset = dataset
        self.model = datamodel
        self.db = self.model(
            'fuels',
            self.model.schema,
            __dbfile__ % self.user
        )
        try:
            self.db.create()
        except Exception as e:
            print('(dont need to create table, because)')
            print('(%s)' % e)

    def add_data(self, data=None):
        self.db.add(
            dict(data)
        )

    def del_data(self, _id=None):
        if not _id:
            _id = input('login>')
        self.db.delete_row_where('_id', _id)

    def get_data(self, _id=None):
        if not _id:
            _id = input('id_>')
        data = self.db.get_row(
            where='_id', equals=_id
        )
        if data:
            ds = self.dataset(
                **data
            )
            return ds
        else:
            print('none found')
            return None

    def list_data(self, _filter=None):
        if not _filter:
            out = self.db.get_summary(
                select='*'
            )
        else:
            out = self.db.get_filter_summary(
                select='*',
                where='_group', like=_filter
            )
        return [self.dataset(**result) for result in out if result]

    def filter(self, where=None):
        def askfor_where():
            print(
                '(possible fields: %s)'
                % ', '.join(
                    self.model.names
                )
            )
            where = input('search in>')
            if where in self.model.names:
                return where
            else:
                askfor_where()

        if not where:
            where = askfor_where()
        else:
            if where not in self.model.names:
                print('invalid field')
                where = askfor_where()

        like = input('search for>')

        if all([where, like]):
            results = [
                self.dataset(**result)
                for result in
                self.db.get_filter_summary(
                    select='_id, _login, _group',
                    where=where, like=like
                ) if result]
            return results

        else:
            print(
                '(consider adding search expression when using filter...)'
            )
            return None

#i = Interactor('graph', FuelModel, Fuel)
#print(i.get_data(1))